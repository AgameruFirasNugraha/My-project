using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.U2D.Sprites;
using UnityEngine;

namespace HollowHill.EditorTools
{
    /// <summary>
    /// Mengatur SEMUA tekstur di Assets/HollowHill/Art secara otomatis saat di-import:
    ///  - Sprite, Pixels Per Unit 182 (1 tile = 1 unit), Point filter, tanpa mipmap, tanpa kompresi
    ///  - Mesh type Full Rect (mencegah celah antar-tile)
    ///  - Pivot pintu "open"/"broken" disetel agar sel pintu tetap pas di grid walau sprite punya overhang
    ///  - Collider dinding berbentuk batang presisi (bukan kotak penuh) lewat Sprite Physics Shape
    /// PENTING: letakkan skrip ini di project SEBELUM menyalin folder Art.
    /// </summary>
    public class HollowHillImporter : AssetPostprocessor
    {
        public const string ArtRoot = "Assets/HollowHill/Art";
        public const int PPU = 182;
        const string OutlineMarker = "hh_wall_outline_v1";

        void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith(ArtRoot) || assetPath.EndsWith("_atlas.png")) return;

            var ti = (TextureImporter)assetImporter;
            bool isFx = assetPath.Contains("/fx/");
            bool isFog = assetPath.Contains("fog_tile");

            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Single;
            ti.spritePixelsPerUnit = PPU;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.filterMode = isFx ? FilterMode.Bilinear : FilterMode.Point;
            ti.wrapMode = isFog ? TextureWrapMode.Repeat : TextureWrapMode.Clamp;
            ti.maxTextureSize = 4096;

            var s = new TextureImporterSettings();
            ti.ReadTextureSettings(s);
            s.spriteMeshType = SpriteMeshType.FullRect;
            s.spriteAlignment = (int)SpriteAlignment.Center;

            Vector2 pivot;
            if (TryDoorPivot(assetPath, out pivot))
            {
                s.spriteAlignment = (int)SpriteAlignment.Custom;
                s.spritePivot = pivot;
            }
            ti.SetTextureSettings(s);
        }

        // Sprite pintu "open"/"broken" lebih besar dari 1 tile (daun pintu terayun keluar dari sel).
        // Sel pintu = 182x182 px di sisi atas (varian _h_) atau sisi kanan (varian _v_).
        static bool TryDoorPivot(string path, out Vector2 pivot)
        {
            pivot = new Vector2(0.5f, 0.5f);
            string n = Path.GetFileNameWithoutExtension(path);
            if (!n.StartsWith("door_") || !(n.Contains("_open") || n.Contains("_broken"))) return false;

            int w, h;
            if (!PngSize(path, out w, out h)) return false;

            if (n.Contains("_h_")) pivot = new Vector2(0.5f, (h - 91f) / h);        // pusat sel = 91 px dari atas
            else if (n.Contains("_v_")) pivot = new Vector2((w - 91f) / w, 0.5f);   // pusat sel = 91 px dari kanan
            else return false;
            return true;
        }

        static bool PngSize(string path, out int w, out int h)
        {
            w = h = 0;
            try
            {
                using (var fs = File.OpenRead(path))
                {
                    var b = new byte[24];
                    if (fs.Read(b, 0, 24) < 24) return false;
                    w = (b[16] << 24) | (b[17] << 16) | (b[18] << 8) | b[19];
                    h = (b[20] << 24) | (b[21] << 16) | (b[22] << 8) | b[23];
                    return w > 0 && h > 0;
                }
            }
            catch { return false; }
        }

        // ------------------------------------------------------------------ collider dinding presisi
        static void OnPostprocessAllAssets(string[] imported, string[] deleted, string[] moved, string[] movedFrom)
        {
            foreach (var path in imported)
            {
                if (!path.StartsWith(ArtRoot) || !path.Contains("/tiles_walls/")) continue;
                string p = path;
                EditorApplication.delayCall += () => ApplyWallOutline(p);
            }
        }

        static int MaskFromName(string n)
        {
            var m = Regex.Match(n, @"^wall_(int|ext|tunnel)_(\d\d)$");
            if (m.Success) return int.Parse(m.Groups[2].Value);
            if (Regex.IsMatch(n, @"^wall_(int|ext|tunnel)_h_dmg\d$")) return 10;
            if (Regex.IsMatch(n, @"^wall_(int|ext|tunnel)_v_dmg\d$")) return 5;
            return -1;
        }

        // Batang dinding setebal 94 px (47 px di tiap sisi pusat), lengan memanjang ke tepi tile (91 px dari pusat).
        static List<Vector2[]> WallOutlines(int mask)
        {
            const float h = 91f, b = 47f;
            var list = new List<Vector2[]> { Rect(-b, -b, b, b) };
            if ((mask & 1) != 0) list.Add(Rect(-b, b, b, h));     // N (atas)
            if ((mask & 2) != 0) list.Add(Rect(b, -b, h, b));     // E (kanan)
            if ((mask & 4) != 0) list.Add(Rect(-b, -h, b, -b));   // S (bawah)
            if ((mask & 8) != 0) list.Add(Rect(-h, -b, -b, b));   // W (kiri)
            return list;
        }

        static Vector2[] Rect(float x0, float y0, float x1, float y1)
        {
            return new[] { new Vector2(x0, y0), new Vector2(x1, y0), new Vector2(x1, y1), new Vector2(x0, y1) };
        }

        static void ApplyWallOutline(string path)
        {
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti == null || ti.userData == OutlineMarker) return;
            int mask = MaskFromName(Path.GetFileNameWithoutExtension(path));
            if (mask < 0) return;

            var factory = new SpriteDataProviderFactories();
            factory.Init();
            var dp = factory.GetSpriteEditorDataProviderFromObject(ti);
            if (dp == null) return;
            dp.InitSpriteEditorDataProvider();
            var outline = dp.GetDataProvider<ISpritePhysicsOutlineDataProvider>();
            foreach (var rect in dp.GetSpriteRects()) outline.SetOutlines(rect.spriteID, WallOutlines(mask));
            dp.Apply();

            ti.userData = OutlineMarker;
            ti.SaveAndReimport();
        }
    }
}
