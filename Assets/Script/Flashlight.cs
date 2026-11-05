using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Rendering.Universal;

public class Flashlight : MonoBehaviour
{
    [SerializeField] private float maxBattery = 100f;
    [SerializeField] private float drainPerSecond = 2f;
    [SerializeField] private float baseIntensity = 1.5f;
    [SerializeField] private float flickerBelow = 25f;

    private Light2D flashlight;
    private float battery;
    private bool isOn = true;

    void Awake()
    {
        flashlight = GetComponent<Light2D>();
        battery = maxBattery;
    }

    void Update()
    {
        if (Keyboard.current.fKey.wasPressedThisFrame && battery > 0f)
        {
            isOn = !isOn;
        }

        if (isOn && battery > 0f)
        {
            battery = Mathf.MoveTowards(battery, 0f, drainPerSecond * Time.deltaTime);
        }

        if (!isOn || battery <= 0f)
        {
            flashlight.intensity = 0f;
            return;
        }

        float intensity = baseIntensity;
        if (battery < flickerBelow)
        {
            intensity = baseIntensity * Random.Range(0.3f, 1f);
        }
        flashlight.intensity = intensity;
    }

    public void AddBattery(float amount)
    {
        battery = Mathf.Min(maxBattery, battery + amount);
    }
}
