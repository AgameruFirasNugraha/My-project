using System.Collections.Generic;
using UnityEngine;

public class EnemyChase : MonoBehaviour
{
    public Transform player;
    public float detectionRange = 5f;
    public float loseRange = 8f;
    public float moveSpeed = 2f;
    public float returnSpeed = 2f;
    public float stopDistance = 0.8f;

    [Header("Anti-Abuse")]
    public float maxPathLength = 15f;   // rute lebih panjang dari ini = dianggap tidak terjangkau
    public float giveUpTime = 1f;       // lama tanpa rute valid sebelum enemy menyerah

    [Header("Pathfinding")]
    public LayerMask obstacleMask;      // layer dinding + props
    public float nodeSize = 0.4f;
    public float agentRadius = 0.25f;
    public float repathInterval = 0.2f;
    public int maxNodes = 4000;

    [Header("Rotasi")]
    public float angleOffset = 0f;
    public float rotateSpeed = 360f;

    Animator anim;
    Vector2 startPos;
    bool chasing, returning;
    List<Vector2> path = new List<Vector2>();
    float repathTimer, noPathTimer;
    Dictionary<Vector2Int, bool> walkCache = new Dictionary<Vector2Int, bool>();

    class Node { public Vector2Int cell; public float g, f; public Node parent; }

    static readonly Vector2Int[] dirs = {
        new Vector2Int(1,0), new Vector2Int(-1,0), new Vector2Int(0,1), new Vector2Int(0,-1),
        new Vector2Int(1,1), new Vector2Int(1,-1), new Vector2Int(-1,1), new Vector2Int(-1,-1) };

    void Start()
    {
        anim = GetComponentInChildren<Animator>();
        startPos = transform.position;
        if (player == null)
        {
            var p = GameObject.FindGameObjectWithTag("Player");
            if (p) player = p.transform;
        }
    }

    void Update()
    {
        if (player == null) return;

        Vector2 pos = transform.position;
        float dist = Vector2.Distance(pos, player.position);
        bool moving = false;

        repathTimer -= Time.deltaTime;
        bool doRepath = repathTimer <= 0f;
        if (doRepath) repathTimer = repathInterval;

        // --- deteksi: harus ada rute valid ke player, bukan sekadar dekat ---
        if (!chasing && doRepath && dist <= detectionRange)
        {
            var p = FindPath(pos, player.position);
            if (p != null) { chasing = true; returning = false; noPathTimer = 0f; path = p; }
        }

        if (chasing && dist > loseRange) { chasing = false; returning = true; path.Clear(); }

        if (chasing)
        {
            if (dist <= stopDistance) Face(player.position - transform.position);
            else
            {
                if (doRepath)
                {
                    var p = FindPath(pos, player.position);
                    if (p != null) { path = p; noPathTimer = 0f; }
                    else
                    {
                        path.Clear();
                        noPathTimer += repathInterval;
                        if (noPathTimer >= giveUpTime) { chasing = false; returning = true; }
                    }
                }
                moving = Follow(moveSpeed);
            }
        }
        else if (returning)
        {
            if (doRepath) path = FindPath(pos, startPos) ?? new List<Vector2> { startPos };
            moving = Follow(returnSpeed);

            if (Vector2.Distance(transform.position, startPos) < 0.1f)
            {
                transform.position = startPos;
                returning = false;
                moving = false;
            }
        }

        if (anim) anim.SetBool("iswalking", moving);
    }

    bool Follow(float speed)
    {
        if (path.Count == 0) return false;

        Vector2 pos = transform.position;
        Vector2 wp = path[0];
        Face(wp - pos);
        transform.position = Vector2.MoveTowards(pos, wp, speed * Time.deltaTime);
        if (Vector2.Distance(transform.position, wp) < 0.05f) path.RemoveAt(0);
        return true;
    }

    // ================= A* =================

    Vector2Int ToCell(Vector2 w) => new Vector2Int(Mathf.RoundToInt(w.x / nodeSize), Mathf.RoundToInt(w.y / nodeSize));
    Vector2 ToWorld(Vector2Int c) => new Vector2(c.x * nodeSize, c.y * nodeSize);

    bool Walkable(Vector2Int c)
    {
        if (walkCache.TryGetValue(c, out bool w)) return w;
        w = Physics2D.OverlapCircle(ToWorld(c), agentRadius, obstacleMask) == null;
        walkCache[c] = w;
        return w;
    }

    bool ClearLine(Vector2 a, Vector2 b)
    {
        Vector2 d = b - a;
        float len = d.magnitude;
        if (len < 0.01f) return true;
        return Physics2D.CircleCast(a, agentRadius, d / len, len, obstacleMask).collider == null;
    }

    float H(Vector2Int a, Vector2Int b)
    {
        int dx = Mathf.Abs(a.x - b.x), dy = Mathf.Abs(a.y - b.y);
        return dx + dy - 0.586f * Mathf.Min(dx, dy);
    }

    // return null kalau tidak terjangkau atau terlalu jauh
    List<Vector2> FindPath(Vector2 from, Vector2 to)
    {
        if (ClearLine(from, to)) return new List<Vector2> { to };

        walkCache.Clear();
        Vector2Int start = ToCell(from), goal = ToCell(to);
        walkCache[start] = true;

        // tujuan di dalam collider (player nempel tembok) -> geser ke sel bebas terdekat
        if (!Walkable(goal))
        {
            bool found = false;
            for (int r = 1; r <= 3 && !found; r++)
                for (int x = -r; x <= r && !found; x++)
                    for (int y = -r; y <= r && !found; y++)
                    {
                        var n = new Vector2Int(goal.x + x, goal.y + y);
                        if (Walkable(n)) { goal = n; found = true; }
                    }
            if (!found) return null;
        }

        var all = new Dictionary<Vector2Int, Node>();
        var closed = new HashSet<Vector2Int>();
        var open = new List<Node>();
        var s = new Node { cell = start, f = H(start, goal) };
        all[start] = s; open.Add(s);

        Node end = null;
        int count = 0;

        while (open.Count > 0 && count++ < maxNodes)
        {
            int bi = 0;
            for (int i = 1; i < open.Count; i++) if (open[i].f < open[bi].f) bi = i;
            Node cur = open[bi];
            open.RemoveAt(bi);

            if (cur.cell == goal) { end = cur; break; }
            closed.Add(cur.cell);

            foreach (var d in dirs)
            {
                var nc = cur.cell + d;
                if (closed.Contains(nc) || !Walkable(nc)) continue;

                bool diag = d.x != 0 && d.y != 0;
                if (diag && (!Walkable(new Vector2Int(cur.cell.x + d.x, cur.cell.y)) ||
                             !Walkable(new Vector2Int(cur.cell.x, cur.cell.y + d.y)))) continue;

                float ng = cur.g + (diag ? 1.414f : 1f);
                if (ng * nodeSize > maxPathLength) continue; // batasi panjang rute

                if (!all.TryGetValue(nc, out Node n))
                {
                    n = new Node { cell = nc, g = ng, f = ng + H(nc, goal), parent = cur };
                    all[nc] = n; open.Add(n);
                }
                else if (ng < n.g)
                {
                    n.g = ng; n.f = ng + H(nc, goal); n.parent = cur;
                    if (!open.Contains(n)) open.Add(n);
                }
            }
        }

        if (end == null) return null;

        var result = new List<Vector2>();
        for (Node n = end; n != null; n = n.parent) result.Add(ToWorld(n.cell));
        result.Reverse();
        result.Add(to);

        // haluskan: lompat ke waypoint terjauh yang bisa dituju lurus
        for (int j = result.Count - 1; j > 0; j--)
            if (ClearLine(from, result[j])) { result.RemoveRange(0, j); break; }

        return result;
    }

    // ================= ROTASI =================

    void Face(Vector2 dir)
    {
        if (dir.sqrMagnitude < 0.0001f) return;
        float a = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg + angleOffset;
        Quaternion t = Quaternion.Euler(0, 0, a);
        transform.rotation = rotateSpeed <= 0f ? t : Quaternion.RotateTowards(transform.rotation, t, rotateSpeed * Time.deltaTime);
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.yellow; Gizmos.DrawWireSphere(transform.position, detectionRange);
        Gizmos.color = Color.red;    Gizmos.DrawWireSphere(transform.position, loseRange);
        if (!Application.isPlaying) return;
        Gizmos.color = Color.cyan;
        Vector3 prev = transform.position;
        foreach (var p in path) { Gizmos.DrawLine(prev, p); prev = p; }
    }
}