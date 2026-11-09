using System.Collections;
using UnityEngine;

public class SceneFadeIn : MonoBehaviour
{
    [SerializeField] private CanvasGroup fadeGroup;
    [SerializeField] private float fadeDuration = 1f;

    private void Awake()
    {
        if (fadeGroup == null)
        {
            Debug.LogError("Assign the Fade From Black Canvas Group in the Inspector.");
            enabled = false;
            return;
        }

        fadeGroup.alpha = 1f;
    }

    private IEnumerator Start()
    {
        float elapsed = 0f;

        while (elapsed < fadeDuration)
        {
            elapsed += Time.unscaledDeltaTime;
            fadeGroup.alpha = 1f - Mathf.Clamp01(elapsed / fadeDuration);
            yield return null;
        }

        fadeGroup.alpha = 0f;
    }
}
