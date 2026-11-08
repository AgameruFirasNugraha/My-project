using System;
using System.Globalization;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace HollowHill
{
    /// <summary>
    /// Lapisan UI ala camcorder: noise VHS berganti frame, titik REC berkedip, jam berjalan dari 02:47:19.
    /// Taruh di Canvas (Screen Space - Overlay) paling atas. Frame noise: fx_vhs_overlay_960x540_0..3.
    /// </summary>
    public class VhsOverlay : MonoBehaviour
    {
        [Header("Noise")]
        public Image noiseImage;
        public Sprite[] noiseFrames;
        public float noiseFps = 12f;

        [Header("Teks")]
        public TMP_Text dateText;
        public TMP_Text timeText;
        public GameObject recDot;
        public float blinkSeconds = 0.6f;

        [Header("Tanggal & jam awal")]
        public int year = 1993, month = 10, day = 31;
        public int startHour = 2, startMinute = 47, startSecond = 19;

        double clock;
        float noiseT, blinkT;
        int frame;

        void Start()
        {
            clock = startHour * 3600 + startMinute * 60 + startSecond;
            if (dateText != null)
                dateText.text = new DateTime(year, month, day).ToString("MMM dd yyyy", CultureInfo.InvariantCulture).ToUpperInvariant();
        }

        void Update()
        {
            clock += Time.unscaledDeltaTime;
            if (timeText != null) timeText.text = TimeSpan.FromSeconds(clock % 86400.0).ToString(@"hh\:mm\:ss");

            blinkT += Time.unscaledDeltaTime;
            if (recDot != null) recDot.SetActive(Mathf.Repeat(blinkT, blinkSeconds * 2f) < blinkSeconds);

            if (noiseImage != null && noiseFrames != null && noiseFrames.Length > 0)
            {
                noiseT += Time.unscaledDeltaTime;
                if (noiseT >= 1f / noiseFps)
                {
                    noiseT = 0f;
                    frame = (frame + UnityEngine.Random.Range(1, noiseFrames.Length)) % noiseFrames.Length;
                    noiseImage.sprite = noiseFrames[frame];
                }
            }
        }
    }
}
