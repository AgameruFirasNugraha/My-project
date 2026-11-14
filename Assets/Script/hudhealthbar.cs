
using UnityEngine;
using UnityEngine.UI;

public class CharacterHUD : MonoBehaviour
{
    [Header("Health")]
    public Image healthBar;
    public float healthSpeed = 5f;

    [Header("Battery / Stamina")]
    public Image batteryBar;
    public float batterySpeed = 5f;

    private float targetHealth = 1f;
    private float targetBattery = 1f;

    private void Update()
    {
        healthBar.fillAmount = Mathf.Lerp(
            healthBar.fillAmount,
            targetHealth,
            healthSpeed * Time.deltaTime
        );

        batteryBar.fillAmount = Mathf.Lerp(
            batteryBar.fillAmount,
            targetBattery,
            batterySpeed * Time.deltaTime
        );
    }

    public void UpdateHealth(int current, int max)
    {
        targetHealth = (float)current / max;
    }

    public void UpdateBattery(float current, float max)
    {
        targetBattery = current / max;
    }
}
