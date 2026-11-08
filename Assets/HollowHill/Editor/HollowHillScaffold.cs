using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.Tilemaps;

namespace HollowHill.EditorTools
{
    public static class HollowHillScaffold
    {
        const string PrefabDir = "Assets/HollowHill/Prefabs";
        const string SettingsDir = "Assets/HollowHill/Settings";

        // ------------------------------------------------------------------ 3) Scaffold peta di scene aktif
        [MenuItem("HollowHill/3 - Create Map Scaffold In Scene")]
        public static void CreateScaffold()
        {
            var root = new GameObject("MAP");
            Undo.RegisterCreatedObjectUndo(root, "Create Map Scaffold");

            var gridGo = new GameObject("Grid");
            gridGo.transform.SetParent(root.transform, false);
            var grid = gridGo.AddComponent<Grid>();
            grid.cellSize = Vector3.one;

            MakeTilemap(gridGo.transform, "Floor", "Floor", 0, false);
            MakeTilemap(gridGo.transform, "Floor_Decals", "Decals", 0, false);
            MakeTilemap(gridGo.transform, "Walls", "Walls", 0, true);
            MakeTilemap(gridGo.transform, "Roof", "Roof", 0, false);

            foreach (var n in new[] { "Props", "Doors", "Lights", "Zones", "Roof_Triggers" })
            {
                var g = new GameObject(n);
                g.transform.SetParent(root.transform, false);
            }

            CreateGlobalLight(root.transform);
            SetupCamera();
            CreateVolume(root.transform);

            Selection.activeGameObject = root;
            Debug.Log("[HollowHill] Scaffold selesai. Simpan scene (Ctrl+S). Berikutnya: menu 4 (pintu) dan 5 (pemain).");
        }

        static Tilemap MakeTilemap(Transform parent, string name, string sortingLayer, int order, bool solid)
        {
            var go = new GameObject(name);
            go.transform.SetParent(parent, false);
            var tm = go.AddComponent<Tilemap>();
            var r = go.AddComponent<TilemapRenderer>();
            r.sortingLayerName = sortingLayer;
            r.sortingOrder = order;

            if (solid)
            {
                var tc = go.AddComponent<TilemapCollider2D>();
                tc.compositeOperation = Collider2D.CompositeOperation.Merge;
                var cc = go.AddComponent<CompositeCollider2D>();      // otomatis menambah Rigidbody2D
                cc.geometryType = CompositeCollider2D.GeometryType.Polygons;
                var rb = go.GetComponent<Rigidbody2D>();
                if (rb != null) rb.bodyType = RigidbodyType2D.Static;
                go.AddComponent<CompositeShadowCaster2D>();
            }
            return tm;
        }

        static void CreateGlobalLight(Transform parent)
        {
            var go = new GameObject("Global Light 2D");
            go.transform.SetParent(parent, false);
            var l = go.AddComponent<Light2D>();
            l.lightType = Light2D.LightType.Global;
            l.intensity = 0.14f;                                  // gelap! cahaya datang dari sumber, bukan dari langit
            l.color = new Color(0.55f, 0.66f, 0.92f);
        }

        static void SetupCamera()
        {
            var cam = Camera.main;
            if (cam == null)
            {
                var camGo = new GameObject("Main Camera");
                camGo.tag = "MainCamera";
                cam = camGo.AddComponent<Camera>();
                camGo.transform.position = new Vector3(0f, 0f, -10f);
            }
            cam.orthographic = true;
            cam.orthographicSize = 1080f / 2f / HollowHillImporter.PPU;
            cam.allowHDR = false;
            cam.allowMSAA = false;
            cam.allowDynamicResolution = false;

            PixelPerfectCamera pp;
            if (!cam.TryGetComponent(out pp)) pp = cam.gameObject.AddComponent<PixelPerfectCamera>();
            pp.assetsPPU = HollowHillImporter.PPU;
            pp.refResolutionX = 1920;
            pp.refResolutionY = 1080;
            pp.gridSnapping = PixelPerfectCamera.GridSnapping.PixelSnapping;   // UpscaleRenderTexture tidak kompatibel dgn post-processing
            pp.cropFrame = PixelPerfectCamera.CropFrame.Windowbox;

            var data = cam.GetUniversalAdditionalCameraData();
            data.renderPostProcessing = true;
        }

        static void CreateVolume(Transform parent)
        {
            HollowHillTilesetBuilder.EnsureFolder(SettingsDir);
            var profile = ScriptableObject.CreateInstance<VolumeProfile>();
            string path = AssetDatabase.GenerateUniqueAssetPath(SettingsDir + "/HollowHill_PostFX.asset");
            AssetDatabase.CreateAsset(profile, path);            // buat aset DULU, baru tambahkan efek

            var bloom = profile.Add<Bloom>();
            bloom.threshold.overrideState = true; bloom.threshold.value = 0.8f;   // kamera SDR: threshold harus < 1
            bloom.intensity.overrideState = true; bloom.intensity.value = 0.6f;
            bloom.scatter.overrideState = true; bloom.scatter.value = 0.65f;

            var vig = profile.Add<Vignette>();
            vig.intensity.overrideState = true; vig.intensity.value = 0.42f;
            vig.smoothness.overrideState = true; vig.smoothness.value = 0.55f;

            var grain = profile.Add<FilmGrain>();
            grain.type.overrideState = true; grain.type.value = FilmGrainLookup.Thin1;
            grain.intensity.overrideState = true; grain.intensity.value = 0.3f;

            var ca = profile.Add<ChromaticAberration>();
            ca.intensity.overrideState = true; ca.intensity.value = 0.18f;

            var col = profile.Add<ColorAdjustments>();
            col.saturation.overrideState = true; col.saturation.value = -22f;
            col.contrast.overrideState = true; col.contrast.value = 12f;

            foreach (var c in profile.components)
                if (c != null && !AssetDatabase.Contains(c)) AssetDatabase.AddObjectToAsset(c, profile);
            EditorUtility.SetDirty(profile);
            AssetDatabase.SaveAssets();

            var go = new GameObject("Global Volume (HollowHill)");
            go.transform.SetParent(parent, false);
            var vol = go.AddComponent<Volume>();
            vol.isGlobal = true;
            vol.sharedProfile = profile;
        }

        // ------------------------------------------------------------------ 4) Prefab pintu
        [MenuItem("HollowHill/4 - Create Door Prefabs")]
        public static void CreateDoors()
        {
            HollowHillTilesetBuilder.EnsureFolder(PrefabDir);
            MakeDoor("Door_Wood_H", "door_wood_h_closed", "door_wood_h_open", false);
            MakeDoor("Door_Wood_V", "door_wood_v_closed", "door_wood_v_open", true);
            MakeDoor("Door_Steel_H", "door_steel_h_closed", "door_steel_h_open", false);
            MakeDoor("Door_Steel_V", "door_steel_v_closed", "door_steel_v_open", true);
            AssetDatabase.SaveAssets(); AssetDatabase.Refresh();
            Debug.Log("[HollowHill] Prefab pintu dibuat di " + PrefabDir + ". Letakkan di sel pintu, dan cat WallConnector di sel yang sama.");
        }

        static void MakeDoor(string prefabName, string closedName, string openName, bool vertical)
        {
            var closed = HollowHillTilesetBuilder.FindSprite(closedName);
            var open = HollowHillTilesetBuilder.FindSprite(openName);
            if (closed == null || open == null)
            {
                Debug.LogWarning("[HollowHill] Sprite pintu tidak ditemukan untuk " + prefabName + " (" + closedName + " / " + openName + ")");
                return;
            }

            var go = new GameObject(prefabName);
            var sr = go.AddComponent<SpriteRenderer>();
            sr.sprite = closed; sr.sortingLayerName = "Walls";

            var box = go.AddComponent<BoxCollider2D>();
            box.size = vertical ? new Vector2(0.52f, 1f) : new Vector2(1f, 0.52f);

            var trig = go.AddComponent<CircleCollider2D>();      // area interaksi, tetap aktif saat pintu terbuka
            trig.isTrigger = true; trig.radius = 0.75f;

            var sc = go.AddComponent<ShadowCaster2D>();          // bentuk bawaan = kotak 1x1 = pas satu sel
            sc.selfShadows = false;

            var door = go.AddComponent<Door2D>();
            door.spriteRenderer = sr; door.closedSprite = closed; door.openSprite = open;
            door.blocker = box; door.shadow = sc;

            PrefabUtility.SaveAsPrefabAsset(go, PrefabDir + "/" + prefabName + ".prefab");
            Object.DestroyImmediate(go);
        }

        // ------------------------------------------------------------------ 5) Rig pemain (placeholder)
        [MenuItem("HollowHill/5 - Create Player Rig (placeholder)")]
        public static void CreatePlayer()
        {
            var sprite = EnsurePlaceholderSprite();

            var root = new GameObject("Player");
            Undo.RegisterCreatedObjectUndo(root, "Create Player");
            var rb = root.AddComponent<Rigidbody2D>();
            rb.gravityScale = 0f; rb.freezeRotation = true;
            var col = root.AddComponent<CircleCollider2D>();
            col.radius = 0.2f;
            var pc = root.AddComponent<PlayerTopDown>();

            var pivot = new GameObject("AimPivot");
            pivot.transform.SetParent(root.transform, false);
            pc.aimPivot = pivot.transform;

            var vis = new GameObject("Visual");
            vis.transform.SetParent(pivot.transform, false);
            var sr = vis.AddComponent<SpriteRenderer>();
            sr.sprite = sprite; sr.sortingLayerName = "Characters";

            var fl = new GameObject("Flashlight");
            fl.transform.SetParent(pivot.transform, false);
            fl.transform.localPosition = new Vector3(0.18f, 0f, 0f);
            fl.transform.localRotation = Quaternion.Euler(0f, 0f, -90f);   // arah Spot 2D = sumbu +Y lokal
            var l = fl.AddComponent<Light2D>();
            l.lightType = Light2D.LightType.Point;                        // di Inspector tampil sebagai "Spot"
            l.color = new Color(1f, 0.95f, 0.8f);
            l.intensity = 1.6f;
            l.pointLightOuterRadius = 7f;
            l.pointLightOuterAngle = 70f;
            l.pointLightInnerAngle = 25f;
            fl.AddComponent<FlashlightController>();

            Selection.activeGameObject = root;
            Debug.Log("[HollowHill] Player dibuat. Aktifkan 'Shadows' pada Light 2D Flashlight di Inspector agar dinding menghalangi cahaya.");
        }

        static Sprite EnsurePlaceholderSprite()
        {
            string dir = HollowHillImporter.ArtRoot + "/placeholders";
            string path = dir + "/player_placeholder.png";
            HollowHillTilesetBuilder.EnsureFolder(dir);

            if (!File.Exists(path))
            {
                const int N = 96;
                var tex = new Texture2D(N, N, TextureFormat.RGBA32, false);
                var clear = new Color32(0, 0, 0, 0);
                var px = new Color32[N * N];
                for (int i = 0; i < px.Length; i++) px[i] = clear;
                for (int y = 0; y < N; y++)
                    for (int x = 0; x < N; x++)
                    {
                        float dx = x - 44f, dy = y - 48f;
                        float d = Mathf.Sqrt(dx * dx + dy * dy);
                        if (d < 30f) px[y * N + x] = new Color32(47, 67, 64, 255);        // badan
                        if (d < 14f) px[y * N + x] = new Color32(200, 168, 136, 255);     // kepala
                        if (x > 60 && x < 92 && Mathf.Abs(y - 48) < (92 - x) * 0.4f) px[y * N + x] = new Color32(68, 77, 86, 255); // senter/lengan menghadap +X
                    }
                tex.SetPixels32(px);
                tex.Apply();
                File.WriteAllBytes(path, tex.EncodeToPNG());
                Object.DestroyImmediate(tex);
                AssetDatabase.ImportAsset(path);
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }
    }
}
