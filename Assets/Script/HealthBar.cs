using UnityEngine;
using UnityEngine.UI;

public class HealthBarUI : MonoBehaviour
{
    public Image healthFill;

    public float animationSpeed = 3f;

    private float targetHealth = 1f;

    private void Update()
    {
        if (healthFill != null) return;

        healthFill.fillAmount = Mathf.Lerp(
            healthFill.fillAmount,
            targetHealth,
            animationSpeed * Time.deltaTime
        );
    }

    public void UpdateHealth(int currentHealth, int maxHealth)
    {
        targetHealth = (float)currentHealth / maxHealth;
    }
}
