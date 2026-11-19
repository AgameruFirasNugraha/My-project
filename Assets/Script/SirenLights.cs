using UnityEngine;
using UnityEngine.Rendering.Universal;

public class SirenLights : MonoBehaviour
{
    [SerializeField] private Light2D redLight;
    [SerializeField] private Light2D blueLight;
    [SerializeField] private float flashesPerSecond = 3f;
    [SerializeField] private float intensity = 2f;
    [SerializeField] private float timeOffset = 0f;

    void Update()
    {
        float t = Mathf.Repeat(Time.time * flashesPerSecond + timeOffset, 2f);
        bool redOn = t < 1f;

        redLight.intensity = redOn ? intensity : 0f;
        blueLight.intensity = redOn ? 0f : intensity;
    }
}
