using System.Collections;
using TMPro;
using UnityEngine;

public class ChapterIntro : MonoBehaviour
{
    [SerializeField] private CanvasGroup overlay;
    [SerializeField] private TMP_Text introText;
    [SerializeField] private AudioSource radioAudio;

    private IEnumerator Start()
    {
        if (overlay == null || introText == null)
        {
            Debug.LogError("ChapterIntro needs an Overlay and Intro Text assigned in the Inspector.");
            yield break;
        }

        overlay.alpha = 1f;
        overlay.interactable = true;
        overlay.blocksRaycasts = true;

        introText.text = "CHAPTER 1\nTHE CALL";
        yield return new WaitForSecondsRealtime(3f);

        introText.text = "RADIO: We lost contact with the east wing. Please investigate.";

        if (radioAudio != null && radioAudio.clip != null)
        {
            radioAudio.Play();
            yield return new WaitForSecondsRealtime(radioAudio.clip.length + 0.5f);
        }
        else
        {
            yield return new WaitForSecondsRealtime(5f);
        }

        introText.text = "OBJECTIVE\nInvestigate the disturbance.";
        yield return new WaitForSecondsRealtime(3f);

        float elapsed = 0f;
        const float fadeDuration = 1f;

        while (elapsed < fadeDuration)
        {
            elapsed += Time.unscaledDeltaTime;
            overlay.alpha = 1f - Mathf.Clamp01(elapsed / fadeDuration);
            yield return null;
        }

        overlay.alpha = 0f;
        overlay.interactable = false;
        overlay.blocksRaycasts = false;
    }
}
