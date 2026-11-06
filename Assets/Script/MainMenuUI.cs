using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenuUI : MonoBehaviour
{
    [SerializeField] private string gameSceneName = "Game";
    [SerializeField] private GameObject mainPanel;
    [SerializeField] private GameObject optionsPanel;

    private void Start()
    {
        if (optionsPanel != null)
            optionsPanel.SetActive(false);
    }

    public void StartGame()
    {
        SceneManager.LoadScene(gameSceneName);
    }

    public void ShowOptions()
    {
        if (mainPanel != null)
            mainPanel.SetActive(false);

        if (optionsPanel != null)
            optionsPanel.SetActive(true);
    }

    public void BackToMenu()
    {
        if (optionsPanel != null)
            optionsPanel.SetActive(false);

        if (mainPanel != null)
            mainPanel.SetActive(true);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}