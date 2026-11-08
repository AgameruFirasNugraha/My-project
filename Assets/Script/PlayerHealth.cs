using UnityEngine;
using UnityEngine.UI;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private float maxHealth = 100f;
    [SerializeField] private Image healthBar;
    [SerializeField] private GameObject deathPanel;
    [SerializeField] private Image damageFlash;
    [SerializeField] private float flashFadeSpeed = 2f;

    private float health;
    private bool dead;

    void Awake()
    {
        Time.timeScale = 1f;
        health = maxHealth;
        dead = false;

        healthBar.fillAmount = 1f;
        deathPanel.SetActive(false);
        SetFlashAlpha(0f);
    }

    void Update()
    {
        if (dead && Keyboard.current.rKey.wasPressedThisFrame)
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }

        if (damageFlash != null && damageFlash.color.a > 0f)
        {
            Color c = damageFlash.color;
            c.a = Mathf.MoveTowards(c.a, 0f, flashFadeSpeed * Time.unscaledDeltaTime);
            damageFlash.color = c;
        }
    }

    public void TakeDamage(float amount)
    {
        if (dead) { return; }

        health = Mathf.Max(0f, health - amount);
        healthBar.fillAmount = health / maxHealth;
        SetFlashAlpha(0.5f);

        if (health <= 0f)
        {
            Die();
        }
    }

    public void Heal(float amount)
    {
        if (dead) { return; }

        health = Mathf.Min(maxHealth, health + amount);
        healthBar.fillAmount = health / maxHealth;
    }

    void Die()
    {
        dead = true;
        deathPanel.SetActive(true);
        Time.timeScale = 0f;
    }

    void SetFlashAlpha(float alpha)
    {
        if (damageFlash == null) { return; }

        Color c = damageFlash.color;
        c.a = alpha;
        damageFlash.color = c;
    }
}
