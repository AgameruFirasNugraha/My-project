using UnityEngine;

public class EnemyChase : MonoBehaviour
{
    public Transform player;
    public float detectionRange = 5f;
    public float loseRange = 8f;
    public float moveSpeed = 2f;
    public float returnSpeed = 2f;
    public float stopDistance = 0.8f;

    [Header("Rotasi")]
    public float angleOffset = 0f;     // samain dengan nilai di EnemyLookAtPlayer sebelumnya
    public float rotateSpeed = 360f;   // 0 = langsung hadap, isi angka biar muternya halus

    private Animator anim;
    private Vector2 startPosition;
    private bool isChasing = false;
    private bool isReturning = false;

    void Start()
    {
        anim = GetComponentInChildren<Animator>();
        startPosition = transform.position;

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag("Player");
            if (p != null) player = p.transform;
        }
    }

    void Update()
    {
        if (player == null) return;

        float dist = Vector2.Distance(transform.position, player.position);
        bool isMoving = false;

        if (!isChasing && dist <= detectionRange)
        {
            isChasing = true;
            isReturning = false;
        }

        if (isChasing && dist > loseRange)
        {
            isChasing = false;
            isReturning = true;
        }

        if (isChasing)
        {
            // Ngadep ke player
            FaceTarget(player.position);

            if (dist > stopDistance)
            {
                transform.position = Vector2.MoveTowards(
                    transform.position, player.position, moveSpeed * Time.deltaTime);
                isMoving = true;
            }
        }
        else if (isReturning)
        {
            // Ngadep ke posisi awal
            FaceTarget(startPosition);

            transform.position = Vector2.MoveTowards(
                transform.position, startPosition, returnSpeed * Time.deltaTime);
            isMoving = true;

            if (Vector2.Distance(transform.position, startPosition) < 0.05f)
            {
                transform.position = startPosition;
                isReturning = false;
                isMoving = false;
            }
        }

        if (anim != null)
            anim.SetBool("iswalking", isMoving);
    }

    void FaceTarget(Vector2 targetPos)
    {
        Vector2 dir = targetPos - (Vector2)transform.position;
        if (dir.sqrMagnitude < 0.0001f) return;

        float angle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg + angleOffset;
        Quaternion target = Quaternion.Euler(0f, 0f, angle);

        if (rotateSpeed <= 0f)
            transform.rotation = target;
        else
            transform.rotation = Quaternion.RotateTowards(
                transform.rotation, target, rotateSpeed * Time.deltaTime);
    }

    void OnDrawGizmosSelected()
    {
        Vector3 center = Application.isPlaying ? (Vector3)startPosition : transform.position;

        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, detectionRange);
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, loseRange);
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(center, 0.2f);
    }
}