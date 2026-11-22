using UnityEngine;
using UnityEngine.Events;

public class EnemyHealth : MonoBehaviour
{
    [SerializeField] private float maxHealth = 50f;
    public UnityEvent onDeath;

    private float health;
    private bool dead;

    void Awake()
    {
        health = maxHealth;
    }

    public void TakeDamage(float amount)
    {
        if (dead) { return; }

        health -= amount;

        if (health <= 0f) { Die(); }
    }

    void Die()
    {
        dead = true;
        onDeath.Invoke();
        Destroy(gameObject);
    }
}