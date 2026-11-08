using UnityEngine;

namespace HollowHill
{
    /// <summary>
    /// Menggeser kabut tanpa celah. Pakai SpriteRenderer dengan Draw Mode = Tiled, sprite fx_fog_tile_512,
    /// material Sprite-Lit-Default (agar kabut hanya tampak di dalam cahaya senter).
    /// </summary>
    [RequireComponent(typeof(SpriteRenderer))]
    public class FogScroller : MonoBehaviour
    {
        public Vector2 speed = new Vector2(0.15f, 0.05f);

        Vector3 start;
        Vector2 tile, offset;

        void Start()
        {
            var sr = GetComponent<SpriteRenderer>();
            start = transform.position;
            Vector3 s = sr.sprite != null ? sr.sprite.bounds.size : Vector3.one;
            tile = new Vector2(s.x * Mathf.Abs(transform.lossyScale.x), s.y * Mathf.Abs(transform.lossyScale.y));
        }

        void Update()
        {
            offset += speed * Time.deltaTime;
            offset.x = Mathf.Repeat(offset.x, tile.x);
            offset.y = Mathf.Repeat(offset.y, tile.y);
            transform.position = start + (Vector3)offset;
        }
    }
}
