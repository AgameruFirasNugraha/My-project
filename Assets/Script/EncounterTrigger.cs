using UnityEngine;

public class EncounterTrigger : MonoBehaviour
{
    [SerializeField] private GameObject enemy;
    [SerializeField] private string message = "";

    private bool triggered;

    void Awake()
    {
        if (enemy != null) { enemy.SetActive(false); }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (triggered) { return; }
        if (other.GetComponentInParent<PlayerHealth>() == null) { return; }

        triggered = true;

        if (enemy != null) { enemy.SetActive(true); }

        if (message != "" && HudMessage.Instance != null)
        {
            HudMessage.Instance.ShowMessage(message);
        }
    }
}
