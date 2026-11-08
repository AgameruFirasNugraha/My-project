using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

namespace HollowHill
{
    /// <summary>Pengatur suasana: warna/intensitas Global Light 2D dan vignette, berpindah halus antar zona.</summary>
    public class AtmosphereManager : MonoBehaviour
    {
        public static AtmosphereManager Instance { get; private set; }

        public Light2D globalLight;
        public Volume volume;
        public float fadeSpeed = 1.2f;

        Color targetColor;
        float targetIntensity, targetVignette;
        Vignette vignette;

        void Awake()
        {
            Instance = this;
            if (globalLight != null) { targetColor = globalLight.color; targetIntensity = globalLight.intensity; }
            if (volume != null && volume.profile != null && volume.profile.TryGet(out vignette))
                targetVignette = vignette.intensity.value;
        }

        public void SetTarget(Color color, float intensity, float vignetteIntensity)
        {
            targetColor = color; targetIntensity = intensity; targetVignette = vignetteIntensity;
        }

        void Update()
        {
            float t = 1f - Mathf.Exp(-fadeSpeed * Time.deltaTime);
            if (globalLight != null)
            {
                globalLight.color = Color.Lerp(globalLight.color, targetColor, t);
                globalLight.intensity = Mathf.Lerp(globalLight.intensity, targetIntensity, t);
            }
            if (vignette != null)
                vignette.intensity.Override(Mathf.Lerp(vignette.intensity.value, targetVignette, t));
        }
    }

    /// <summary>Trigger zona. Makin jauh dari lobi -> makin gelap (Kirkbride: pasien terberat di ujung sayap).
    /// Pemain harus punya komponen HHPlayerHooks.</summary>
    [RequireComponent(typeof(Collider2D))]
    public class ZoneAtmosphere : MonoBehaviour
    {
        public Color lightColor = new Color(0.30f, 0.38f, 0.55f);
        [Range(0f, 1.5f)] public float intensity = 0.12f;
        [Range(0f, 1f)] public float vignette = 0.4f;

        void Reset() { GetComponent<Collider2D>().isTrigger = true; }

        void OnTriggerEnter2D(Collider2D c)
        {
            if (c.GetComponentInParent<HHPlayerHooks>() == null) return;
            if (AtmosphereManager.Instance != null) AtmosphereManager.Instance.SetTarget(lightColor, intensity, vignette);
        }
    }
}
