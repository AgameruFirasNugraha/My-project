using UnityEngine;
using UnityEngine.Tilemaps;

namespace HollowHill
{
    /// <summary>
    /// Satu tile yang memilih sprite acak (stabil per posisi) dari beberapa varian.
    /// Memecah pola berulang lantai tanpa Anda mengecat varian satu per satu.
    /// </summary>
    [CreateAssetMenu(menuName = "HollowHill/Variant Tile", fileName = "VariantTile")]
    public class VariantTile : TileBase
    {
        public Sprite[] variants;
        public Tile.ColliderType colliderType = Tile.ColliderType.None;

        public override void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)
        {
            if (variants == null || variants.Length == 0) return;
            int h = Hash(position.x, position.y);
            tileData.sprite = variants[h % variants.Length];
            tileData.color = Color.white;
            tileData.colliderType = colliderType;
            tileData.flags = TileFlags.LockAll;
        }

        static int Hash(int x, int y)
        {
            unchecked
            {
                int h = x * 73856093 ^ y * 19349663;
                h ^= h >> 13; h *= 1274126177; h ^= h >> 16;
                return h & 0x7fffffff;
            }
        }
    }
}
