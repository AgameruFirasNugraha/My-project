using System.Collections;
using TMPro;
using UnityEngine;

public class HudMessage : MonoBehaviour
{
    public static HudMessage Instance;

    [SerializeField] private TMP_Text text;
    [SerializeField] private float messageTime = 1.5f;

    private string promptText = "";
    private object promptOwner;
    private bool showingMessage;

    void Awake()
    {
        Instance = this;
        text.text = "";
    }

    public void ShowPrompt(string message, object source)
    {
        promptOwner = source;
        promptText = message;

        if (!showingMessage)
        {
            text.text = promptText;
        }
    }

    public void HidePrompt(object source)
    {
        if (promptOwner != source) { return; }

        promptOwner = null;
        promptText = "";

        if (!showingMessage)
        {
            text.text = "";
        }
    }

    public void ShowMessage(string message)
    {
        StopAllCoroutines();
        StartCoroutine(MessageRoutine(message));
    }

    IEnumerator MessageRoutine(string message)
    {
        showingMessage = true;
        text.text = message;

        yield return new WaitForSeconds(messageTime);

        showingMessage = false;
        text.text = promptText;
    }
}
