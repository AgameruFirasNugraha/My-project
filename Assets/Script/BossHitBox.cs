using UnityEngine;

public class BossHitbox : MonoBehaviour
{
    private BossStats stats;
    private bool hitThisDash;

    void Awake() { stats = GetComponentInParent<BossStats>(); }
    void OnEnable() { hitThisDash = false; }   // reset tiap dash

    void OnTriggerEnter2D(Collider2D other)
    {
        if (hitThisDash || !other.CompareTag("Player")) return;

        var target = other.GetComponentInParent<IDamageable>();
        if (target != null)
        {
            target.TakeDamage(stats.Damage);   // damage ikut zona
            hitThisDash = true;                // 1 dash = max 1 hit
        }
    }
}