using System.Collections;
using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace HollowHill
{
    public enum FlickerMode { Steady, Neon, Candle, FailingBulb }

    /// <summary>Lampu berkedip. Neon = jarang tapi menegangkan. FailingBulb = hampir selalu mati.</summary>
    [RequireComponent(typeof(Light2D))]
    public class FlickerLight2D : MonoBehaviour
    {
        public FlickerMode mode = FlickerMode.Neon;
        public float baseIntensity = 1f;

        [Header("Sprite lampu (opsional)")]
        public SpriteRenderer lampRenderer;
        public Sprite spriteOn, spriteDim, spriteOff;

        [Header("Audio (opsional)")]
        public AudioSource buzz;

        Light2D lamp;
        float seed;

        void Awake()
        {
            lamp = GetComponent<Light2D>();
            seed = Random.value * 100f;
        }

        void OnEnable()
        {
            if (mode == FlickerMode.Neon) StartCoroutine(NeonRoutine());
            else if (mode == FlickerMode.FailingBulb) StartCoroutine(FailingRoutine());
            else Set(1f, spriteOn);
        }

        void Update()
        {
            if (mode != FlickerMode.Candle) return;
            float n = Mathf.PerlinNoise(Time.time * 6f, seed);
            lamp.intensity = baseIntensity * Mathf.Lerp(0.65f, 1.1f, n);
        }

        IEnumerator NeonRoutine()
        {
            Set(1f, spriteOn);
            while (true)
            {
                yield return new WaitForSeconds(Random.Range(2f, 7f));
                int bursts = Random.Range(2, 6);
                for (int i = 0; i < bursts; i++)
                {
                    bool off = Random.value < 0.5f;
                    Set(off ? 0f : 0.35f, off ? spriteOff : spriteDim);
                    yield return new WaitForSeconds(Random.Range(0.03f, 0.12f));
                    Set(1f, spriteOn);
                    yield return new WaitForSeconds(Random.Range(0.03f, 0.15f));
                }
            }
        }

        IEnumerator FailingRoutine()
        {
            while (true)
            {
                Set(0f, spriteOff);
                yield return new WaitForSeconds(Random.Range(0.8f, 3.5f));
                int n = Random.Range(1, 4);
                for (int i = 0; i < n; i++)
                {
                    Set(0.7f, spriteDim);
                    yield return new WaitForSeconds(Random.Range(0.05f, 0.2f));
                    Set(0f, spriteOff);
                    yield return new WaitForSeconds(Random.Range(0.05f, 0.15f));
                }
            }
        }

        void Set(float k, Sprite s)
        {
            lamp.intensity = baseIntensity * k;
            if (lampRenderer != null && s != null) lampRenderer.sprite = s;
            if (buzz != null) buzz.volume = k > 0.5f ? 0.6f : 0f;
        }
    }
}
