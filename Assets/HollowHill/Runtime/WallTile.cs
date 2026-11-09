using UnityEngine;
using UnityEngine.Tilemaps;

namespace HollowHill
{
    /// <summary>
    /// Autotile dinding 16-bitmask. Tetangga N=1, E=2, S=4, W=8 (Unity: N = +Y).
    /// Index sprites[mask] sama persis dengan penamaan wall_int_XX dari Sprite Kit.
    /// </summary>
    [CreateAssetMenu(menuName = "HollowHill/Wall Tile (16 mask)", fileName = "WallTile")]
    public class WallTile : TileBase
    {
        [Tooltip("Index = mask. N=1, E=2, S=4, W=8")]
        public Sprite[] sprites = new Sprite[16];

        [Header("Variasi rusak (opsional)")]
        public Sprite[] damagedHorizontal;   // dipakai untuk mask 10 (lurus kiri-kanan)
        public Sprite[] damagedVertical;     // dipakai untuk mask 5 (lurus atas-bawah)
        [Range(0f, 1f)] public float damageChance = 0.12f;

        [Header("Khusus sel pintu")]
        [Tooltip("Tidak punya gambar & collider. Hanya 'menyambung' dinding di sebelahnya.")]
        public bool invisibleConnector;

        public Tile.ColliderType colliderType = Tile.ColliderType.Sprite;

        public override void RefreshTile(Vector3Int position, ITilemap tilemap)
        {
            base.RefreshTile(position, tilemap);
            tilemap.RefreshTile(position + Vector3Int.up);
            tilemap.RefreshTile(position + Vector3Int.right);
            tilemap.RefreshTile(position + Vector3Int.down);
            tilemap.RefreshTile(position + Vector3Int.left);
        }

        public override void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)
        {
            int mask = 0;
            if (Connects(tilemap, position + Vector3Int.up)) mask |= 1;
            if (Connects(tilemap, position + Vector3Int.right)) mask |= 2;
            if (Connects(tilemap, position + Vector3Int.down)) mask |= 4;
            if (Connects(tilemap, position + Vector3Int.left)) mask |= 8;

            tileData.color = Color.white;
            tileData.flags = TileFlags.LockTransform | TileFlags.LockColor;
            tileData.transform = Matrix4x4.identity;

            if (invisibleConnector)
            {
                tileData.sprite = null;
                tileData.colliderType = Tile.ColliderType.None;
                return;
            }

            tileData.sprite = PickSprite(mask, position);
            tileData.colliderType = colliderType;
        }

        static bool Connects(ITilemap tilemap, Vector3Int p)
        {
            return tilemap.GetTile(p) is WallTile;
        }

        Sprite PickSprite(int mask, Vector3Int p)
        {
            if (damageChance > 0f)
            {
                Sprite[] pool = mask == 10 ? damagedHorizontal : (mask == 5 ? damagedVertical : null);
                if (pool != null && pool.Length > 0 && Hash01(p.x, p.y) < damageChance)
                {
                    int idx = (int)(Hash01(p.x + 17, p.y + 31) * pool.Length);
                    return pool[Mathf.Clamp(idx, 0, pool.Length - 1)];
                }
            }
            return (sprites != null && mask < sprites.Length) ? sprites[mask] : null;
        }

        static float Hash01(int x, int y)
        {
            unchecked
            {
                int h = x * 73856093 ^ y * 19349663;
                h ^= h >> 13; h *= 1274126177; h ^= h >> 16;
                return (h & 0x7fffffff) / (float)int.MaxValue;
            }
        }
    }
}
