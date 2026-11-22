using UnityEngine;
using UnityEngine.Events;
using UnityEngine.InputSystem;

public class ReadableNote : MonoBehaviour
{
    [SerializeField] private string title = "Bloody Note";
    [SerializeField, TextArea(3, 8)] private string body = "The building is compromised, save yourselves.";
    public UnityEvent onFinishedReading;

    private bool playerInside;
    private bool finished;

    void Update()
    {
        if (!playerInside) { return; }
        if (NoteReaderUI.IsOpen) { return; }
        if (Time.frameCount == NoteReaderUI.ClosedFrame) { return; }

        if (Keyboard.current.eKey.wasPressedThisFrame)
        {
            Read();
        }
    }

    void Read()
    {
        if (NoteReaderUI.Instance == null) { return; }

        if (HudMessage.Instance != null) { HudMessage.Instance.HidePrompt(this); }

        NoteReaderUI.Instance.Open(title, body, OnClosed);
    }

    void OnClosed()
    {
        if (!finished)
        {
            finished = true;
            onFinishedReading.Invoke();
        }

        if (playerInside && HudMessage.Instance != null)
        {
            HudMessage.Instance.ShowPrompt("[E] Read note", this);
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null) { return; }

        playerInside = true;

        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.ShowPrompt("[E] Read note", this);
        }
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null) { return; }

        playerInside = false;

        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.HidePrompt(this);
        }
    }

    void OnDestroy()
    {
        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.HidePrompt(this);
        }
    }
}