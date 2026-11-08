using UnityEngine;

public class EnemyAttack : MonoBehaviour
{
    public int damage = 10;
    public float attackCooldown = 1f;

    private float nextAttackTime = 0f;

    void OnTriggerStay2D(Collider2D other)
    {
        // Masih dalam jeda, jangan serang dulu
        if (Time.time < nextAttackTime) return;

        PlayerHealth health = other.GetComponentInParent<PlayerHealth>();
        if (health != null)
        {
            health.TakeDamage(damage);
            nextAttackTime = Time.time + attackCooldown;
            Debug.Log("Player kena damage: " + damage);
        }
    }
}