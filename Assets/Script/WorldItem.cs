using UnityEngine;

public class WorldItem : MonoBehaviour
{
    [SerializeField] private ItemData item;

    private InventoryUI inventory;

    void Start()
    {
        inventory = FindAnyObjectByType<InventoryUI>();
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.GetComponent<PlayerHealth>() == null)
        {
            return;
        }

        if (inventory.AddItem(item))
        {
            Destroy(gameObject);
        }
    }
}