using System.Collections.Generic;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace HollowHill.EditorTools
{
    /// <summary>
    /// Membuat Shadow Caster 2D dari jalur Composite Collider 2D tilemap dinding, agar senter & lampu
    /// tidak tembus tembok. Shadow Caster 2D tidak punya API publik untuk menyetel bentuk, jadi kita menyetel
    /// field serial-nya lewat reflection. Kalau Unity mengubah nama field, skrip memberi tahu Anda dengan jelas
    /// (lihat "Jika gagal" di README).
    /// Jalankan ULANG setiap kali Anda selesai mengubah dinding.
    /// </summary>
    public static class TilemapShadowBuilder
    {
        const string ChildPrefix = "ShadowPath_";

        [MenuItem("HollowHill/6 - Rebuild Shadow Casters (select Walls tilemap)")]
        public static void Rebuild()
        {
            var go = Selection.activeGameObject;
            CompositeCollider2D comp = null;
            if (go == null || !go.TryGetComponent(out comp))
            {
                EditorUtility.DisplayDialog("HollowHill", "Pilih GameObject 'Walls' (yang punya Composite Collider 2D) di Hierarchy dulu.", "OK");
                return;
            }

            FieldInfo fPath = typeof(ShadowCaster2D).GetField("m_ShapePath", BindingFlags.NonPublic | BindingFlags.Instance);
            FieldInfo fHash = typeof(ShadowCaster2D).GetField("m_ShapePathHash", BindingFlags.NonPublic | BindingFlags.Instance);
            if (fPath == null || fHash == null)
            {
                Debug.LogError("[HollowHill] Field internal ShadowCaster2D (m_ShapePath / m_ShapePathHash) tidak ditemukan di versi URP ini. " +
                               "Gunakan skrip resmi 'ShadowCaster2DGenerator' dari forum Unity (cari: Script for generating ShadowCaster2Ds for Tilemaps) " +
                               "atau kirim versi Unity Anda ke saya.");
                return;
            }

            comp.GenerateGeometry();
            Undo.IncrementCurrentGroup();

            for (int i = go.transform.childCount - 1; i >= 0; i--)
            {
                var c = go.transform.GetChild(i);
                if (c.name.StartsWith(ChildPrefix)) Undo.DestroyObjectImmediate(c.gameObject);
            }

            CompositeShadowCaster2D existing;
            if (!go.TryGetComponent(out existing)) Undo.AddComponent<CompositeShadowCaster2D>(go);

            var pts = new List<Vector2>();
            int made = 0;
            for (int i = 0; i < comp.pathCount; i++)
            {
                pts.Clear();
                comp.GetPath(i, pts);
                if (pts.Count < 3) continue;

                var v3 = new Vector3[pts.Count];
                for (int k = 0; k < pts.Count; k++) v3[k] = pts[k];

                var child = new GameObject(ChildPrefix + i);
                Undo.RegisterCreatedObjectUndo(child, "Shadow Path");
                child.transform.SetParent(go.transform, false);

                var sc = child.AddComponent<ShadowCaster2D>();
                sc.selfShadows = false;               // puncak dinding tetap terang; ruangan tetap terang dari dalam
                fPath.SetValue(sc, v3);
                fHash.SetValue(sc, Hash(v3));         // hash baru = Unity membangun ulang mesh bayangan
                made++;
            }

            EditorSceneManager.MarkSceneDirty(go.scene);
            Debug.Log("[HollowHill] " + made + " jalur bayangan dibuat. Simpan scene. Pastikan Light 2D Anda mencentang 'Shadows'.");
        }

        static int Hash(Vector3[] v)
        {
            unchecked
            {
                uint h = 2166136261;
                for (int i = 0; i < v.Length; i++)
                {
                    h = (h ^ (uint)v[i].x.GetHashCode()) * 16777619;
                    h = (h ^ (uint)v[i].y.GetHashCode()) * 16777619;
                }
                return (int)(h & 0x7fffffff);
            }
        }
    }
}
