using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.InputSystem;

public class InventoryUI : MonoBehaviour
{
    [SerializeField] private GameObject panel;
    [SerializeField] private Transform slotGrid;
    [SerializeField] private GameObject slotPrefab;
    [SerializeField] private int slotCount = 15;
    [SerializeField] private PlayerHealth playerHealth;
    [SerializeField] private Flashlight flashlight;

    private List<ItemData> items = new List<ItemData>();
    private List<Image> icons = new List<Image>();

    void Start()
    {
        for (int i = 0; i < slotCount; i++)
        {
            GameObject slot = Instantiate(slotPrefab, slotGrid);

            Image icon = slot.transform.GetChild(0).GetComponent<Image>();
            icon.enabled = false;

            items.Add(null);
            icons.Add(icon);

            int index = i;
            slot.GetComponent<Button>().onClick.AddListener(() => UseItem(index));
        }

        panel.SetActive(false);
    }

    void Update()
    {
        if (Keyboard.current.tabKey.wasPressedThisFrame)
        {
            panel.SetActive(!panel.activeSelf);
        }
    }

    public bool AddItem(ItemData item)
    {
        for (int i = 0; i < items.Count; i++)
        {
            if (items[i] == null)
            {
                items[i] = item;
                icons[i].sprite = item.icon;
                icons[i].color = item.color;
                icons[i].enabled = true;
                return true;
            }
        }
        return false;
    }

    void UseItem(int index)
    {
        ItemData item = items[index];
        if (item == null) { return; }

        if (item.healAmount > 0 && playerHealth != null)
        {
            playerHealth.Heal(item.healAmount);
        }

        if (item.batteryAmount > 0 && flashlight != null)
        {
            flashlight.AddBattery(item.batteryAmount);
        }

        items[index] = null;
        icons[index].enabled = false;
    }
}