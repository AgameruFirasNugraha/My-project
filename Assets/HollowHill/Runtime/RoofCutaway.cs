using UnityEngine;
using UnityEngine.Tilemaps;

namespace HollowHill
{
    /// <summary>
    /// Atap memudar saat pemain masuk gedung ("atap yang terbuka"). Pasang di objek dengan Collider2D (Is Trigger)
    /// yang menutupi bagian dalam gedung, lalu isi daftar sprite/tilemap atap.
    /// Pemain harus punya komponen HHPlayerHooks.
    /// </summary>
    [RequireComponent(typeof(Collider2D))]
    public class RoofCutaway : MonoBehaviour
    {
        public SpriteRenderer[] roofSprites;
        public Tilemap[] roofTilemaps;
        public float fadeSeconds = 0.7f;
        [Range(0f, 1f)] public float insideAlpha = 0f;

        float current = 1f, target = 1f;

        void Reset() { GetComponent<Collider2D>().isTrigger = true; }

        void OnTriggerEnter2D(Collider2D c) { if (c.GetComponentInParent<HHPlayerHooks>() != null) target = insideAlpha; }
        void OnTriggerExit2D(Collider2D c) { if (c.GetComponentInParent<HHPlayerHooks>() != null) target = 1f; }

        void Update()
        {
            if (Mathf.Approximately(current, target)) return;
            current = Mathf.MoveTowards(current, target, Time.deltaTime / Mathf.Max(0.01f, fadeSeconds));
            if (roofSprites != null)
                foreach (var s in roofSprites) if (s != null) { var c = s.color; c.a = current; s.color = c; }
            if (roofTilemaps != null)
                foreach (var t in roofTilemaps) if (t != null) t.color = new Color(1f, 1f, 1f, current);
        }
    }
}
