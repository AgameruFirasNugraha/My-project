using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Tilemaps;

namespace HollowHill.EditorTools
{
    public static class HollowHillTilesetBuilder
    {
        const string Art = HollowHillImporter.ArtRoot;
        const string Out = "Assets/HollowHill/Tiles";

        // ------------------------------------------------------------------ 1) Setup proyek
        [MenuItem("HollowHill/1 - Project Setup (Sorting Layers, Quality)")]
        public static void ProjectSetup()
        {
            // Urutan = urutan gambar (bawah -> atas)
            string[] layers = { "Floor", "Decals", "Props", "Characters", "Walls", "Overhead", "Roof", "FX" };

            var assets = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset");
            if (assets == null || assets.Length == 0) { Debug.LogError("[HollowHill] TagManager.asset tidak ditemukan."); return; }
            var tagManager = new SerializedObject(assets[0]);
            var sl = tagManager.FindProperty("m_SortingLayers");

            foreach (var name in layers)
            {
                bool found = false;
                for (int i = 0; i < sl.arraySize; i++)
                    if (sl.GetArrayElementAtIndex(i).FindPropertyRelative("name").stringValue == name) { found = true; break; }
                if (found) continue;

                sl.InsertArrayElementAtIndex(sl.arraySize);
                var e = sl.GetArrayElementAtIndex(sl.arraySize - 1);
                e.FindPropertyRelative("name").stringValue = name;
                e.FindPropertyRelative("uniqueID").intValue = StableId(name);
                e.FindPropertyRelative("locked").boolValue = false;
            }
            tagManager.ApplyModifiedProperties();

            QualitySettings.antiAliasing = 0;                       // AA memburamkan tepi piksel
            QualitySettings.anisotropicFiltering = AnisotropicFiltering.Disable;
            Physics2D.gravity = Vector2.zero;                       // top-down: tidak ada gravitasi

            AssetDatabase.SaveAssets();
            Debug.Log("[HollowHill] Sorting layers dibuat: " + string.Join(", ", layers) +
                      ". Gravity 2D = 0, AA = 0. LANGKAH MANUAL: matikan MSAA di URP Asset (lihat panduan).");
        }

        static int StableId(string s)
        {
            unchecked
            {
                uint h = 2166136261;
                foreach (char c in s) { h ^= c; h *= 16777619; }
                return (int)(h & 0x7fffffff);
            }
        }

        // ------------------------------------------------------------------ 2) Bangun aset tile
        static readonly Dictionary<string, string[]> Families = new Dictionary<string, string[]>
        {
            { "Floor_Parquet_Mixed",   new[] { "floor_parquet_a", "floor_parquet_a", "floor_parquet_b", "floor_parquet_rotted" } },
            { "Floor_Lino_Mixed",      new[] { "floor_lino_a", "floor_lino_b", "floor_lino_worn", "floor_lino_peeled" } },
            { "Floor_Hex_Mixed",       new[] { "floor_hex_a", "floor_hex_a", "floor_hex_b", "floor_hex_ruined" } },
            { "Floor_Morgue_Mixed",    new[] { "floor_morgue_a", "floor_morgue_b" } },
            { "Floor_Concrete_Mixed",  new[] { "floor_conc_a", "floor_conc_a", "floor_conc_wet" } },
            { "Floor_Grass_Mixed",     new[] { "floor_grass_a", "floor_grass_b", "floor_grass_c" } },
            { "Floor_GrassDead_Mixed", new[] { "floor_grass_dead_a", "floor_grass_dead_b", "floor_cemetery_grass" } },
            { "Floor_Pavers_Mixed",    new[] { "floor_pavers_a", "floor_pavers_a", "floor_pavers_mossy" } },
            { "Floor_Dirt_Mixed",      new[] { "floor_dirt_a", "floor_dirt_b" } },
            { "Floor_Asphalt_Mixed",   new[] { "floor_asphalt_a", "floor_asphalt_b" } },
        };

        [MenuItem("HollowHill/2 - Build Tile Assets")]
        public static void BuildTiles()
        {
            EnsureFolder(Out); EnsureFolder(Out + "/Floors"); EnsureFolder(Out + "/Walls");
            int made = 0;

            // a) satu Tile per sprite lantai (kontrol penuh saat mengecat)
            foreach (var dir in new[] { "tiles_floor_interior", "tiles_floor_exterior" })
            {
                foreach (var sp in LoadSprites(Art + "/" + dir))
                {
                    var t = LoadOrCreate<Tile>(Out + "/Floors/" + sp.name + ".asset");
                    t.sprite = sp; t.colliderType = Tile.ColliderType.None;
                    EditorUtility.SetDirty(t); made++;
                }
            }

            // b) tile varian acak (memecah pola berulang)
            foreach (var kv in Families)
            {
                var list = new List<Sprite>();
                foreach (var n in kv.Value) { var sp = FindSprite(n); if (sp != null) list.Add(sp); }
                if (list.Count == 0) continue;
                var v = LoadOrCreate<HollowHill.VariantTile>(Out + "/Floors/" + kv.Key + ".asset");
                v.variants = list.ToArray();
                EditorUtility.SetDirty(v); made++;
            }

            // c) dinding autotile (3 gaya) + konektor tak terlihat untuk sel pintu
            foreach (var style in new[] { "wall_int", "wall_ext", "wall_tunnel" })
            {
                var w = LoadOrCreate<HollowHill.WallTile>(Out + "/Walls/" + Pretty(style) + ".asset");
                w.sprites = new Sprite[16];
                for (int m = 0; m < 16; m++) w.sprites[m] = FindSprite(style + "_" + m.ToString("00"));
                w.damagedHorizontal = FindMany(style + "_h_dmg", 3);
                w.damagedVertical = FindMany(style + "_v_dmg", 3);
                w.colliderType = Tile.ColliderType.Sprite;
                EditorUtility.SetDirty(w); made++;
            }
            var conn = LoadOrCreate<HollowHill.WallTile>(Out + "/Walls/Wall_DoorConnector.asset");
            conn.invisibleConnector = true; conn.damageChance = 0f;
            EditorUtility.SetDirty(conn); made++;

            AssetDatabase.SaveAssets(); AssetDatabase.Refresh();
            Debug.Log("[HollowHill] " + made + " aset tile dibuat/diperbarui di " + Out +
                      ". Sekarang buat Tile Palette dan seret isi folder Tiles ke dalamnya.");
        }

        static string Pretty(string style)
        {
            switch (style)
            {
                case "wall_int": return "Wall_Interior";
                case "wall_ext": return "Wall_Exterior";
                default: return "Wall_Tunnel";
            }
        }

        // ------------------------------------------------------------------ helper
        public static Sprite FindSprite(string name)
        {
            foreach (var guid in AssetDatabase.FindAssets(name + " t:Sprite", new[] { Art }))
            {
                string p = AssetDatabase.GUIDToAssetPath(guid);
                if (Path.GetFileNameWithoutExtension(p) == name) return AssetDatabase.LoadAssetAtPath<Sprite>(p);
            }
            return null;
        }

        static Sprite[] FindMany(string prefix, int count)
        {
            var list = new List<Sprite>();
            for (int i = 0; i < count; i++) { var s = FindSprite(prefix + i); if (s != null) list.Add(s); }
            return list.ToArray();
        }

        static IEnumerable<Sprite> LoadSprites(string folder)
        {
            if (!AssetDatabase.IsValidFolder(folder)) yield break;
            foreach (var guid in AssetDatabase.FindAssets("t:Sprite", new[] { folder }))
            {
                var sp = AssetDatabase.LoadAssetAtPath<Sprite>(AssetDatabase.GUIDToAssetPath(guid));
                if (sp != null) yield return sp;
            }
        }

        static T LoadOrCreate<T>(string path) where T : ScriptableObject
        {
            var existing = AssetDatabase.LoadAssetAtPath<T>(path);
            if (existing != null) return existing;
            var created = ScriptableObject.CreateInstance<T>();
            AssetDatabase.CreateAsset(created, path);
            return created;
        }

        public static void EnsureFolder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            string parent = Path.GetDirectoryName(path).Replace("\\", "/");
            if (!AssetDatabase.IsValidFolder(parent)) EnsureFolder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }
    }
}
