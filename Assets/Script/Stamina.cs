using UnityEngine;
using UnityEngine.UI;

public class Stamina : MonoBehaviour
{
    [Header("Amounts")]
    [SerializeField] private float maxStamina = 100f;
    [SerializeField] private float drainPerSecond = 22f;
    [SerializeField] private float regenPerSecond = 12f;
    [SerializeField] private float regenDelay = 1f;
    [SerializeField] private float recoverAt = 30f;

    [Header("Bar")]
    [SerializeField] private Image fillImage;
    [SerializeField] private Color normalColor = Color.white;
    [SerializeField] private Color exhaustedColor = new Color(1f, 0.35f, 0.35f);
    [SerializeField] private float barStart = 0f;
    [SerializeField] private float barEnd = 1f;

    private float current;
    private float regenTimer;
    private bool exhausted;

    public bool CanSprint
    {
        get { return !exhausted && current > 0f; }
    }

    public float Percent
    {
        get { return current / maxStamina; }
    }

    void Awake()
    {
        current = maxStamina;
        UpdateBar();
    }

    public void Tick(bool sprinting)
    {
        if (sprinting && CanSprint)
        {
            current -= drainPerSecond * Time.deltaTime;
            regenTimer = regenDelay;

            if (current <= 0f)
            {
                current = 0f;
                exhausted = true;
            }
        }
        else
        {
            if (regenTimer > 0f)
            {
                regenTimer -= Time.deltaTime;
            }
            else
            {
                current = Mathf.Min(maxStamina, current + regenPerSecond * Time.deltaTime);
            }

            if (exhausted && current >= recoverAt)
            {
                exhausted = false;
            }
        }

        UpdateBar();
    }

    void UpdateBar()
    {
        if (fillImage == null) { return; }

        float percent = Mathf.Clamp01(current / maxStamina);

        fillImage.fillAmount = Mathf.Lerp(barStart, barEnd, percent);
        fillImage.color = exhausted ? exhaustedColor : normalColor;
    }
}