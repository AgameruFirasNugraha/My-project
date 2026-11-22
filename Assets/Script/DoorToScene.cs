using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

public class DoorToScene : MonoBehaviour
{
    [SerializeField] private string sceneName = "Map Inside";
    [SerializeField] private bool locked = true;
    [SerializeField] private string lockedMessage = "The door is locked.";
    [SerializeField] private CanvasGroup fadeGroup;
    [SerializeField] private float fadeDuration = 0.8f;

    private bool playerInside;
    private bool transitioning;

    public void Unlock()
    {
        locked = false;

        if (playerInside)
        {
            ShowPrompt();
        }
    }

    private void Update()
    {
        if (!playerInside || transitioning)
        {
            return;
        }

        if (Keyboard.current.eKey.wasPressedThisFrame)
        {
            if (locked)
            {
                if (HudMessage.Instance != null)
                {
                    HudMessage.Instance.ShowMessage(lockedMessage);
                }
            }
            else
            {
                StartCoroutine(FadeAndLoadScene());
            }
        }
    }

    private IEnumerator FadeAndLoadScene()
    {
        if (fadeGroup == null)
        {
            Debug.LogError("Assign the Fade From Black Canvas Group in the Inspector.", this);
            yield break;
        }

        transitioning = true;
        fadeGroup.blocksRaycasts = true;

        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.HidePrompt(this);
        }

        float elapsed = 0f;

        while (elapsed < fadeDuration)
        {
            elapsed += Time.unscaledDeltaTime;
            fadeGroup.alpha = Mathf.Clamp01(elapsed / fadeDuration);
            yield return null;
        }

        SceneManager.LoadScene(sceneName);
    }

    private void ShowPrompt()
    {
        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.ShowPrompt("[E] Enter building", this);
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null)
        {
            return;
        }

        playerInside = true;
        ShowPrompt();
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null)
        {
            return;
        }

        playerInside = false;

        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.HidePrompt(this);
        }
    }

    private void OnDestroy()
    {
        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.HidePrompt(this);
        }
    }
}