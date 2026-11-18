using UnityEngine;
using UnityEngine.InputSystem;

public class WorldItem : MonoBehaviour
{
    [SerializeField] private ItemData item;
    [SerializeField] private GameObject prompt;

    private InventoryUI inventory;
    private bool playerInside;

    void Start()
    {
        inventory = FindAnyObjectByType<InventoryUI>();

        if (prompt != null) { prompt.SetActive(false); }
    }

    void Update()
    {
        if (playerInside && Keyboard.current.eKey.wasPressedThisFrame)
        {
            TryPickUp();
        }
    }

    void TryPickUp()
    {
        if (inventory == null) { return; }

        if (inventory.AddItem(item))
        {
            Destroy(gameObject);
        }
        else
        {
            if (HudMessage.Instance != null)
            {
                HudMessage.Instance.ShowMessage("Backpack full");
            }
            else
            {
                Debug.Log("Backpack full");
            }
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null) { return; }

        playerInside = true;

        if (prompt != null) { prompt.SetActive(true); }

        if (HudMessage.Instance != null)
        {
            HudMessage.Instance.ShowPrompt("[E] Pick up " + item.itemName, this);
        }
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (other.GetComponentInParent<PlayerHealth>() == null) { return; }

        playerInside = false;

        if (prompt != null) { prompt.SetActive(false); }

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