using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Chapter2Intro : MonoBehaviour
{
    [SerializeField] private CanvasGroup overlay;
    [SerializeField] private TMP_Text introText;
    [SerializeField] private AudioSource radioAudio;
    [SerializeField] private string nextSceneName = "Map Inside";

    private IEnumerator Start()
    {
        if (overlay == null || introText == null)
        {
            Debug.LogError("Assign the Overlay and Intro Text.", this);
            yield break;
        }

        overlay.alpha = 1f;
        overlay.interactable = true;
        overlay.blocksRaycasts = true;

        introText.text = "CHAPTER 2\nTHE WARDS";
        yield return new WaitForSecondsRealtime(3f);

        introText.text =
            "No one’s coming. I’ll clear the ground floor, find a key, and get upstairs. One room at a time.";

    if (radioAudio != null && radioAudio.clip != null)
    {
        radioAudio.Play();
        yield return new WaitForSecondsRealtime(radioAudio.clip.length);
    }
    else
    {
        yield return new WaitForSecondsRealtime(4f);
    }

        introText.text = "OBJECTIVE\nClear the ground-floor rooms.\nFind the stairwell key.";
        yield return new WaitForSecondsRealtime(3f);

        SceneManager.LoadScene(nextSceneName);
    }
}