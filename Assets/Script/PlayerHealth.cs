using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

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
        health = maxHealth;
        Time.timeScale = 1f;
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

        if (damageFlash.color.a > 0f)
        {
            float alpha = Mathf.MoveTowards(damageFlash.color.a, 0f, flashFadeSpeed * Time.unscaledDeltaTime);
            SetFlashAlpha(alpha);
        }
    }

    public void TakeDamage(float amount)
    {
        if (dead)
        {
            return;
        }

        health = Mathf.MoveTowards(health, 0f, amount);
        healthBar.fillAmount = health / maxHealth;
        SetFlashAlpha(0.5f);

        if (health <= 0f)
        {
            dead = true;
            Time.timeScale = 0f;
            deathPanel.SetActive(true);
        }
    }

    private void SetFlashAlpha(float alpha)
    {
        Color c = damageFlash.color;
        c.a = alpha;
        damageFlash.color = c;
    }
}
