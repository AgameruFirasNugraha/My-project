using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace HollowHill
{
    /// <summary>
    /// Senter: F = nyala/mati, klik kanan = fokus (sempit, jauh, boros). Baterai habis -> berkedip lalu mati.
    /// Pasang di anak Player yang punya Light2D tipe Spot (enum: Point). Arah cahaya = sumbu lokal +Y,
    /// jadi putar objek ini -90 derajat di dalam AimPivot (dibuat otomatis oleh menu Create Player Rig).
    /// </summary>
    [RequireComponent(typeof(Light2D))]
    public class FlashlightController : MonoBehaviour
    {
        [Header("Cahaya (satuan = tile)")]
        public float normalRadius = 7f;
        public float focusRadius = 10f;
        public float normalAngle = 70f;
        public float focusAngle = 28f;
        public float intensity = 1.6f;

        [Header("Baterai")]
        public float batterySeconds = 180f;
        public float drainWhileOn = 1f;
        public float drainWhileFocus = 2.2f;
        [Range(0f, 1f)] public float lowBatteryAt = 0.2f;

        public bool IsOn { get; private set; }
        public float Battery01 { get { return batterySeconds <= 0f ? 0f : battery / batterySeconds; } }
        public event System.Action<float> BatteryChanged;

        Light2D lamp;
        float battery, focus, seed;

        void Awake()
        {
            lamp = GetComponent<Light2D>();
            battery = batterySeconds;
            IsOn = true;
            seed = Random.value * 100f;
        }

        void Update()
        {
            if (HHInput.FlashlightToggleDown() && battery > 0f) IsOn = !IsOn;

            bool focusing = IsOn && HHInput.FocusHeld();
            focus = Mathf.MoveTowards(focus, focusing ? 1f : 0f, Time.deltaTime * 6f);

            if (IsOn)
            {
                float drain = Mathf.Lerp(drainWhileOn, drainWhileFocus, focus);
                battery = Mathf.Max(0f, battery - drain * Time.deltaTime);
                if (BatteryChanged != null) BatteryChanged(Battery01);
                if (battery <= 0f) IsOn = false;
            }

            lamp.enabled = IsOn;
            float outer = Mathf.Lerp(normalAngle, focusAngle, focus);
            float radius = Mathf.Lerp(normalRadius, focusRadius, focus);
            lamp.pointLightOuterAngle = outer;
            lamp.pointLightInnerAngle = outer * 0.35f;
            lamp.pointLightOuterRadius = radius;
            lamp.pointLightInnerRadius = radius * 0.08f;

            float k = 1f;
            if (Battery01 < lowBatteryAt)
            {
                float n = Mathf.PerlinNoise(Time.time * 18f, seed);
                float dying = Mathf.Lerp(0.4f, 1f, Battery01 / Mathf.Max(0.0001f, lowBatteryAt));
                k = (n > 0.35f ? 1f : Mathf.Lerp(0.05f, 0.5f, n / 0.35f)) * dying;
            }
            lamp.intensity = intensity * k;
        }

        public void AddBattery(float seconds)
        {
            battery = Mathf.Min(batterySeconds, battery + seconds);
            if (battery > 0f && !IsOn) IsOn = true;
        }
    }
}
