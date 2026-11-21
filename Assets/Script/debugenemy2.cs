using UnityEngine;

public class ChaseDebug : MonoBehaviour
{
    public LayerMask obstacleMask;   // isi sama dengan di EnemyChase
    public float nodeSize = 0.4f;
    public float agentRadius = 0.25f;
    public int range = 12;           // jumlah sel di sekitar enemy yang digambar

    void Start()
    {
        Debug.Log("Mask value: " + obstacleMask.value + " (0 = belum diisi)");
    }

    void OnDrawGizmos()
    {
        Vector2 o = transform.position;
        for (int x = -range; x <= range; x++)
            for (int y = -range; y <= range; y++)
            {
                Vector2 p = new Vector2(Mathf.Round(o.x / nodeSize + x) * nodeSize,
                                        Mathf.Round(o.y / nodeSize + y) * nodeSize);
                bool blocked = Physics2D.OverlapCircle(p, agentRadius, obstacleMask) != null;
                Gizmos.color = blocked ? new Color(1, 0, 0, 0.6f) : new Color(0, 1, 0, 0.15f);
                Gizmos.DrawCube(p, Vector3.one * nodeSize * 0.8f);
            }
    }
}