using UnityEngine;

public class EnemyLookAtPlayer : MonoBehaviour
{
    public Transform player;
    public float angleOffset = 0f;   // koreksi arah default sprite
    public float rotateSpeed = 0f;   // 0 = langsung hadap, isi mis. 360 biar muternya halus

    void Start()
    {
        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag("Player");
            if (p != null) player = p.transform;
        }
    }

    void Update()
    {
        if (player == null) return;

        Vector2 dir = player.position - transform.position;
        float angle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg + angleOffset;
        Quaternion target = Quaternion.Euler(0f, 0f, angle);

        if (rotateSpeed <= 0f)
            transform.rotation = target;
        else
            transform.rotation = Quaternion.RotateTowards(transform.rotation, target, rotateSpeed * Time.deltaTime);
    }
}