using UnityEngine;

// Pasang di object "Boss_Spawn". Menggambar lingkaran batas zona di lantai (petunjuk abstraction).
public class ZoneRings : MonoBehaviour
{
    public BossStats boss;                 // kosong = dicari otomatis
    public int segments = 64;
    public float lineWidth = 0.08f;
    public int sortingOrder = 1;
    // warna ring = warna zona yang DIMASUKI di balik ring itu (kuning, lalu merah)
    public Color[] ringColors = { new Color(1f, 0.9f, 0.3f, 0.55f), new Color(1f, 0.3f, 0.3f, 0.55f) };

    void Start()
    {
        if (boss == null) boss = FindFirstObjectByType<BossStats>();
        if (boss == null) { Debug.LogWarning("[ZoneRings] BossStats tidak ditemukan"); return; }

        for (int i = 0; i < boss.zoneLimits.Length; i++)
        {
            Color c = ringColors[Mathf.Min(i, ringColors.Length - 1)];
            CreateRing(boss.zoneLimits[i] * boss.maxDistance, c);
        }
    }

    void CreateRing(float radius, Color c)
    {
        var go = new GameObject("Ring_" + radius.ToString("0"));
        go.transform.SetParent(transform, false);
        var lr = go.AddComponent<LineRenderer>();
        lr.useWorldSpace = false;
        lr.loop = true;
        lr.positionCount = segments;
        lr.startWidth = lr.endWidth = lineWidth;
        lr.material = new Material(Shader.Find("Sprites/Default"));
        lr.startColor = lr.endColor = c;
        lr.sortingOrder = sortingOrder;

        for (int i = 0; i < segments; i++)
        {
            float a = i * Mathf.PI * 2f / segments;
            lr.SetPosition(i, new Vector3(Mathf.Cos(a) * radius, Mathf.Sin(a) * radius, 0f));
        }
    }
}