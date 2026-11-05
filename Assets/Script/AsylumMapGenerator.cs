using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class AsylumMapGenerator : MonoBehaviour
{
    [Header("Tilemaps")]
    public Tilemap floorTilemap;
    public Tilemap wallTilemap;
    public Tilemap overlayTilemap;

    [Header("Tiles Utama")]
    public TileBase floorTile;
    public TileBase wallTile;
    public TileBase stairTile;
    public TileBase doorTile; // Pasang Tile Pintu di sini (Opsional)

    [Header("Tiles Dekorasi Horor")]
    public TileBase[] bloodTiles;
    public TileBase[] debrisTiles;
    [Range(0, 100)] public int horrorDecalChance = 15;

    [Header("Pengaturan Multi-Lantai")]
    public int totalFloors = 3;
    public int floorWidth = 100;
    public int floorHeight = 100;
    public int maxRoomsPerFloor = 18;
    public int floorSpacingY = 120;

    [Header("Prefabs & Entity")]
    public GameObject playerPrefab;
    public GameObject enemyPrefab;
    public GameObject doorPrefab; // Pasang Prefab Pintu jika ingin pintu berupa objek interaktif (Opsional)
    public int enemiesPerRoom = 2;

    private int totalGridWidth;
    private int totalGridHeight;
    private int[,] mapData; // 0 = Kosong, 1 = Lantai, 2 = Dinding, 3 = Tangga, 4 = Pintu
    private Dictionary<int, List<RectInt>> floorRooms = new Dictionary<int, List<RectInt>>();

    void Start()
    {
        GenerateAsylum();
    }

    public void GenerateAsylum()
    {
        floorTilemap.ClearAllTiles();
        wallTilemap.ClearAllTiles();
        if (overlayTilemap != null) overlayTilemap.ClearAllTiles();
        floorRooms.Clear();

        totalGridWidth = floorWidth;
        totalGridHeight = floorSpacingY * totalFloors;
        mapData = new int[totalGridWidth, totalGridHeight];

        // 1. Generate Ruangan & Lorong
        for (int f = 0; f < totalFloors; f++)
        {
            GenerateSingleFloor(f);
        }

        // 2. Sambungkan Tangga Antar Lantai
        ConnectFloorsWithStairs();

        // 3. Cari dan Deteksi Pintu Masuk Setiap Ruangan
        GenerateDoors();

        // 4. Buat Pembatas Dinding
        GenerateWalls();

        // 5. Render Visual Tilemap
        RenderMap();

        // 6. Spawn Player, Enemy & Prefab Pintu
        SpawnEntities();
    }

    void GenerateSingleFloor(int floorIndex)
    {
        List<RectInt> currentFloorRooms = new List<RectInt>();
        int offsetY = floorIndex * floorSpacingY;

        for (int i = 0; i < maxRoomsPerFloor; i++)
        {
            bool isIsolationCell = Random.value < 0.3f;
            int roomW = isIsolationCell ? Random.Range(4, 6) : Random.Range(8, 15);
            int roomH = isIsolationCell ? Random.Range(4, 6) : Random.Range(8, 15);

            int roomX = Random.Range(3, floorWidth - roomW - 3);
            int roomY = offsetY + Random.Range(3, floorHeight - roomH - 3);

            RectInt newRoom = new RectInt(roomX, roomY, roomW, roomH);

            bool overlaps = false;
            foreach (var room in currentFloorRooms)
            {
                if (newRoom.Overlaps(room)) { overlaps = true; break; }
            }

            if (!overlaps)
            {
                CreateRoom(newRoom);

                if (currentFloorRooms.Count > 0)
                {
                    Vector2Int prevCenter = Vector2Int.RoundToInt(currentFloorRooms[currentFloorRooms.Count - 1].center);
                    Vector2Int newCenter = Vector2Int.RoundToInt(newRoom.center);
                    CreateCorridor(prevCenter, newCenter);
                }

                currentFloorRooms.Add(newRoom);
            }
        }
        floorRooms.Add(floorIndex, currentFloorRooms);
    }

    void CreateRoom(RectInt room)
    {
        for (int x = room.xMin; x < room.xMax; x++)
        {
            for (int y = room.yMin; y < room.yMax; y++)
            {
                mapData[x, y] = 1;
            }
        }
    }

    void CreateCorridor(Vector2Int start, Vector2Int end)
    {
        int currentX = start.x;
        int currentY = start.y;

        while (currentX != end.x)
        {
            mapData[currentX, currentY] = 1;
            if (currentY + 1 < totalGridHeight - 1) mapData[currentX, currentY + 1] = 1;
            currentX += (end.x > currentX) ? 1 : -1;
        }

        while (currentY != end.y)
        {
            mapData[currentX, currentY] = 1;
            if (currentX + 1 < totalGridWidth - 1) mapData[currentX + 1, currentY] = 1;
            currentY += (end.y > currentY) ? 1 : -1;
        }
    }

    void ConnectFloorsWithStairs()
    {
        for (int f = 0; f < totalFloors - 1; f++)
        {
            List<RectInt> currentRooms = floorRooms[f];
            if (currentRooms.Count > 0)
            {
                Vector2Int stairPos = Vector2Int.RoundToInt(currentRooms[currentRooms.Count - 1].center);
                mapData[stairPos.x, stairPos.y] = 3;
            }
        }
    }

    void GenerateDoors()
    {
        HashSet<Vector2Int> doorPositions = new HashSet<Vector2Int>();

        foreach (var floorKvp in floorRooms)
        {
            foreach (var room in floorKvp.Value)
            {
                // Periksa batas bawah ruangan
                for (int x = room.xMin; x < room.xMax; x++)
                {
                    int y = room.yMin;
                    if (mapData[x, y] == 1 && y - 1 >= 0 && mapData[x, y - 1] == 1)
                        doorPositions.Add(new Vector2Int(x, y));
                }
                // Periksa batas atas ruangan
                for (int x = room.xMin; x < room.xMax; x++)
                {
                    int y = room.yMax - 1;
                    if (mapData[x, y] == 1 && y + 1 < totalGridHeight && mapData[x, y + 1] == 1)
                        doorPositions.Add(new Vector2Int(x, y));
                }
                // Periksa batas kiri ruangan
                for (int y = room.yMin; y < room.yMax; y++)
                {
                    int x = room.xMin;
                    if (mapData[x, y] == 1 && x - 1 >= 0 && mapData[x - 1, y] == 1)
                        doorPositions.Add(new Vector2Int(x, y));
                }
                // Periksa batas kanan ruangan
                for (int y = room.yMin; y < room.yMax; y++)
                {
                    int x = room.xMax - 1;
                    if (mapData[x, y] == 1 && x + 1 < totalGridWidth && mapData[x + 1, y] == 1)
                        doorPositions.Add(new Vector2Int(x, y));
                }
            }
        }

        // Tandai posisi pintu (4) jika area tersebut bukan tangga
        foreach (var pos in doorPositions)
        {
            if (mapData[pos.x, pos.y] == 1)
            {
                mapData[pos.x, pos.y] = 4;
            }
        }
    }

    void GenerateWalls()
    {
        for (int x = 0; x < totalGridWidth; x++)
        {
            for (int y = 0; y < totalGridHeight; y++)
            {
                if (mapData[x, y] == 0 && HasAdjacentFloorOrStair(x, y))
                {
                    mapData[x, y] = 2;
                }
            }
        }
    }

    bool HasAdjacentFloorOrStair(int x, int y)
    {
        for (int dx = -1; dx <= 1; dx++)
        {
            for (int dy = -1; dy <= 1; dy++)
            {
                if (dx == 0 && dy == 0) continue;
                int nx = x + dx;
                int ny = y + dy;
                if (nx >= 0 && nx < totalGridWidth && ny >= 0 && ny < totalGridHeight)
                {
                    if (mapData[nx, ny] == 1 || mapData[nx, ny] == 3 || mapData[nx, ny] == 4) return true;
                }
            }
        }
        return false;
    }

    void RenderMap()
    {
        for (int x = 0; x < totalGridWidth; x++)
        {
            for (int y = 0; y < totalGridHeight; y++)
            {
                Vector3Int tilePos = new Vector3Int(x, y, 0);

                if (mapData[x, y] == 1)
                {
                    floorTilemap.SetTile(tilePos, floorTile);

                    if (overlayTilemap != null && Random.Range(0, 100) < horrorDecalChance)
                    {
                        if (bloodTiles != null && bloodTiles.Length > 0 && Random.value > 0.5f)
                        {
                            floorTilemap.SetTile(tilePos, floorTile);
                            overlayTilemap.SetTile(tilePos, bloodTiles[Random.Range(0, bloodTiles.Length)]);
                        }
                        else if (debrisTiles != null && debrisTiles.Length > 0)
                        {
                            overlayTilemap.SetTile(tilePos, debrisTiles[Random.Range(0, debrisTiles.Length)]);
                        }
                    }
                }
                else if (mapData[x, y] == 2)
                {
                    wallTilemap.SetTile(tilePos, wallTile);
                }
                else if (mapData[x, y] == 3)
                {
                    floorTilemap.SetTile(tilePos, stairTile != null ? stairTile : floorTile);
                }
                else if (mapData[x, y] == 4)
                {
                    // Pasang lantai dasar terlebih dahulu di bawah pintu
                    floorTilemap.SetTile(tilePos, floorTile);

                    // Pasang Tile Pintu jika dimasukkan di Inspector
                    if (doorTile != null)
                    {
                        wallTilemap.SetTile(tilePos, doorTile);
                    }
                }
            }
        }
    }

    void SpawnEntities()
    {
        // Clean up entity lama
        GameObject oldPlayer = GameObject.FindGameObjectWithTag("Player");
        if (oldPlayer != null) Destroy(oldPlayer);

        GameObject[] oldEnemies = GameObject.FindGameObjectsWithTag("Enemy");
        foreach (var e in oldEnemies) Destroy(e);

        GameObject[] oldDoors = GameObject.FindGameObjectsWithTag("Door");
        foreach (var d in oldDoors) Destroy(d);

        // Spawn Player di ruangan pertama
        if (floorRooms.ContainsKey(0) && floorRooms[0].Count > 0)
        {
            Vector2 playerPos = floorRooms[0][0].center;
            if (playerPrefab != null)
                Instantiate(playerPrefab, new Vector3(playerPos.x, playerPos.y, 0), Quaternion.identity);
        }

        // Spawn Enemy
        if (enemyPrefab != null)
        {
            for (int f = 0; f < totalFloors; f++)
            {
                List<RectInt> rooms = floorRooms[f];
                int startRoomIndex = (f == 0) ? 1 : 0;

                for (int i = startRoomIndex; i < rooms.Count; i++)
                {
                    for (int e = 0; e < enemiesPerRoom; e++)
                    {
                        float rx = Random.Range(rooms[i].xMin + 1, rooms[i].xMax - 1);
                        float ry = Random.Range(rooms[i].yMin + 1, rooms[i].yMax - 1);
                        Instantiate(enemyPrefab, new Vector3(rx, ry, 0), Quaternion.identity);
                    }
                }
            }
        }

        // Spawn Prefab Pintu (jika menggunakan Prefab)
        if (doorPrefab != null)
        {
            for (int x = 0; x < totalGridWidth; x++)
            {
                for (int y = 0; y < totalGridHeight; y++)
                {
                    if (mapData[x, y] == 4)
                    {
                        Vector3 doorWorldPos = floorTilemap.GetCellCenterWorld(new Vector3Int(x, y, 0));
                        Instantiate(doorPrefab, doorWorldPos, Quaternion.identity);
                    }
                }
            }
        }
    }
}