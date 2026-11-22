using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class InventoryItem
{
    public ItemData data;
    public int x;
    public int y;
    public bool rotated;
    public int amount;
    public ItemView view;

    public int Width { get { return rotated ? data.height : data.width; } }
    public int Height { get { return rotated ? data.width : data.height; } }
}

public class InventoryUI : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private GameObject panel;
    [SerializeField] private RectTransform gridArea;
    [SerializeField] private GameObject cellPrefab;
    [SerializeField] private ItemView itemPrefab;
    [SerializeField] private PlayerHealth playerHealth;
    [SerializeField] private Flashlight flashlight;
    [SerializeField] private TMP_Text infoName;
    [SerializeField] private TMP_Text infoDescription;

    [Header("Grid")]
    [SerializeField] private int columns = 6;
    [SerializeField] private int rows = 3;
    [SerializeField] private float cellSize = 110f;
    [SerializeField] private float spacing = 6f;

    [Header("Start")]
    [SerializeField] private ItemData startingMagazine;
    [SerializeField] private int startingMagazines = 2;

    public event System.Action Changed;

    public bool IsOpen => panel != null && panel.activeSelf;
    public RectTransform GridArea => gridArea;

    private List<InventoryItem> items = new List<InventoryItem>();

    void Awake()
{
    BuildGrid();

    if (startingMagazine != null)
    {
        for (int i = 0; i < startingMagazines; i++)
        {
            AddItem(startingMagazine);
        }
    }

    ClearInfo();
    panel.SetActive(false);
}

    void BuildGrid()
    {
        gridArea.sizeDelta = new Vector2(
            columns * cellSize + (columns - 1) * spacing,
            rows * cellSize + (rows - 1) * spacing);

        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < columns; c++)
            {
                GameObject cell = Instantiate(cellPrefab, gridArea);
                RectTransform rt = (RectTransform)cell.transform;

                rt.anchorMin = new Vector2(0f, 1f);
                rt.anchorMax = new Vector2(0f, 1f);
                rt.pivot = new Vector2(0f, 1f);
                rt.sizeDelta = new Vector2(cellSize, cellSize);
                rt.anchoredPosition = new Vector2(c * (cellSize + spacing), -r * (cellSize + spacing));
            }
        }
    }

    void Update()
    {
        if (Keyboard.current.tabKey.wasPressedThisFrame)
        {
            if (!panel.activeSelf && Time.timeScale == 0f) { return; }

            bool open = !panel.activeSelf;
            panel.SetActive(open);
            Time.timeScale = open ? 0f : 1f;
            ClearInfo();
        }
    }

    public bool AddItem(ItemData data)
    {
        int x;
        int y;
        bool rotated = false;

        if (!FindSpace(data.width, data.height, null, out x, out y))
        {
            if (data.width == data.height || !FindSpace(data.height, data.width, null, out x, out y))
            {
                return false;
            }

            rotated = true;
        }

        InventoryItem item = new InventoryItem();
        item.data = data;
        item.x = x;
        item.y = y;
        item.rotated = rotated;
        item.amount = data.isMagazine ? data.magazineRounds : 0;

        ItemView view = Instantiate(itemPrefab, gridArea);
        view.Setup(this, item, cellSize, spacing);
        item.view = view;

        items.Add(item);
        Changed?.Invoke();
        return true;
    }

    bool FindSpace(int w, int h, InventoryItem ignore, out int foundX, out int foundY)
    {
        for (int y = 0; y <= rows - h; y++)
        {
            for (int x = 0; x <= columns - w; x++)
            {
                if (Fits(x, y, w, h, ignore))
                {
                    foundX = x;
                    foundY = y;
                    return true;
                }
            }
        }

        foundX = 0;
        foundY = 0;
        return false;
    }

    bool Fits(int x, int y, int w, int h, InventoryItem ignore)
    {
        if (x < 0 || y < 0 || x + w > columns || y + h > rows) { return false; }

        foreach (InventoryItem other in items)
        {
            if (other == ignore) { continue; }

            bool overlap = other.x < x + w && other.x + other.Width > x
                        && other.y < y + h && other.y + other.Height > y;

            if (overlap) { return false; }
        }

        return true;
    }

    public bool CanPlace(InventoryItem item, int x, int y)
    {
        return Fits(x, y, item.Width, item.Height, item);
    }

    public void PlaceItem(InventoryItem item, int x, int y)
    {
        item.x = x;
        item.y = y;
        item.view.Refresh();
        Changed?.Invoke();
    }

    public void UseItem(InventoryItem item)
    {
        if (item.data.isMagazine) { return; }

        if (item.data.healAmount > 0 && playerHealth != null)
        {
            playerHealth.Heal(item.data.healAmount);
        }

        if (item.data.batteryAmount > 0 && flashlight != null)
        {
            flashlight.AddBattery(item.data.batteryAmount);
        }

        RemoveItem(item);
    }

    void RemoveItem(InventoryItem item)
    {
        if (item.view != null) { Destroy(item.view.gameObject); }

        items.Remove(item);
        ClearInfo();
        Changed?.Invoke();
    }

    public void ShowInfo(InventoryItem item)
    {
        if (infoName != null) { infoName.text = item.data.itemName; }
        if (infoDescription != null) { infoDescription.text = item.data.description; }
    }

    public void ClearInfo()
    {
        if (infoName != null) { infoName.text = ""; }
        if (infoDescription != null) { infoDescription.text = ""; }
    }

    public int MagazineCount()
    {
        int count = 0;

        foreach (InventoryItem item in items)
        {
            if (item.data.isMagazine) { count++; }
        }

        return count;
    }

    InventoryItem FindFullestMagazine()
    {
        InventoryItem best = null;

        foreach (InventoryItem item in items)
        {
            if (item.data.isMagazine && item.amount > 0 && (best == null || item.amount > best.amount))
            {
                best = item;
            }
        }

        return best;
    }

    public bool HasBetterMagazine(int currentRounds)
    {
        InventoryItem best = FindFullestMagazine();
        return best != null && best.amount > currentRounds;
    }

    public bool SwapMagazine(int currentRounds, out int newRounds)
    {
        newRounds = 0;
        InventoryItem best = FindFullestMagazine();

        string log = "Gun has " + currentRounds + ". Bag: ";
        foreach (InventoryItem item in items)
        {
            if (item.data.isMagazine) { log += item.amount + " "; }
        }
        Debug.Log(log);

        if (best == null || best.amount <= currentRounds) { return false; }

        newRounds = best.amount;

        if (currentRounds > 0)
        {
            best.amount = currentRounds;
            best.view.Refresh();
            Changed?.Invoke();
        }
        else
        {
        RemoveItem(best);
        }

    return true;
 }
}