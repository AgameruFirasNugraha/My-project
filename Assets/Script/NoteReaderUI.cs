using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class NoteReaderUI : MonoBehaviour
{
    public static NoteReaderUI Instance;
    public static bool IsOpen;
    public static int ClosedFrame = -1;

    [SerializeField] private GameObject panel;
    [SerializeField] private TMP_Text titleText;
    [SerializeField] private TMP_Text bodyText;

    private System.Action onClose;
    private int openedFrame;

    void Awake()
    {
        Instance = this;
        IsOpen = false;
        panel.SetActive(false);
    }

    void OnDestroy()
    {
        if (Instance == this)
        {
            Instance = null;
            IsOpen = false;
        }
    }

    public void Open(string title, string body, System.Action closeCallback)
    {
        titleText.text = title;
        bodyText.text = body;
        onClose = closeCallback;

        panel.SetActive(true);
        IsOpen = true;
        Time.timeScale = 0f;
        openedFrame = Time.frameCount;
    }

    void Update()
    {
        if (!IsOpen) { return; }
        if (Time.frameCount == openedFrame) { return; }

        if (Keyboard.current.eKey.wasPressedThisFrame || Keyboard.current.escapeKey.wasPressedThisFrame)
        {
            Close();
        }
    }

    void Close()
    {
        panel.SetActive(false);
        IsOpen = false;
        ClosedFrame = Time.frameCount;
        Time.timeScale = 1f;

        System.Action callback = onClose;
        onClose = null;

        if (callback != null) { callback(); }
    }
}