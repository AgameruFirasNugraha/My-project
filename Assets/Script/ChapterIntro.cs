using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ChapterIntro : MonoBehaviour
{
    [SerializeField] private CanvasGroup overlay;
    [SerializeField] private TMP_Text introText;
    [SerializeField] private AudioSource radioAudio;
    [SerializeField] private string nextSceneName = "Game";

    private IEnumerator Start()
    {
        if (overlay == null || introText == null)
        {
            Debug.LogError("ChapterIntro needs its Overlay and Intro Text assigned.");
            yield break;
        }

        overlay.alpha = 1f;
        overlay.interactable = true;
        overlay.blocksRaycasts = true;

        introText.text = "CHAPTER 1\nTHE CALL";
        yield return new WaitForSecondsRealtime(3f);

        introText.text =
            "RADIO: Unit 12, this is dispatch. We've had a report of a disturbance in the east wing. Staff are on site. Check in at reception before entering the ward. Call us when you arrive.";

        if (radioAudio != null && radioAudio.clip != null)
        {
            radioAudio.Play();
            yield return new WaitForSecondsRealtime(radioAudio.clip.length + 0.5f);
        }
        else
        {
            Debug.LogWarning("Radio Audio or its clip is not assigned. Showing the radio subtitle for 5 seconds.");
            yield return new WaitForSecondsRealtime(5f);
        }

        introText.text = "OBJECTIVE\nInvestigate the disturbance.";
        yield return new WaitForSecondsRealtime(3f);

        SceneManager.LoadScene(nextSceneName);
    }
}
