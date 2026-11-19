using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.UI;


public class ItemView : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler,
    IBeginDragHandler, IDragHandler, IEndDragHandler
{
    [SerializeField] private Image icon;
    [SerializeField] private TMP_Text amountText;

    private InventoryUI inventory;
    private InventoryItem item;
    private float cellSize;
    private float spacing;

    private Image background;
    private Color normalColor;

    private bool dragging;
    private bool originalRotated;
    private int targetX;
    private int targetY;

    public void Setup(InventoryUI owner, InventoryItem inventoryItem, float cell, float space)
    {
        inventory = owner;
        item = inventoryItem;
        cellSize = cell;
        spacing = space;

        background = GetComponent<Image>();
        normalColor = background.color;

        icon.sprite = item.data.icon;
        icon.color = item.data.color;

        Refresh();
    }

    public void Refresh()
    {
        icon.preserveAspect = true;
        
        RectTransform rt = (RectTransform)transform;
        rt.anchorMin = new Vector2(0f, 1f);
        rt.anchorMax = new Vector2(0f, 1f);
        rt.pivot = new Vector2(0f, 1f);

        float w = item.Width * cellSize + (item.Width - 1) * spacing;
        float h = item.Height * cellSize + (item.Height - 1) * spacing;

        rt.sizeDelta = new Vector2(w, h);
        rt.anchoredPosition = new Vector2(item.x * (cellSize + spacing), -item.y * (cellSize + spacing));

        RectTransform iconRect = icon.rectTransform;
        iconRect.anchorMin = new Vector2(0.5f, 0.5f);
        iconRect.anchorMax = new Vector2(0.5f, 0.5f);
        iconRect.pivot = new Vector2(0.5f, 0.5f);
        iconRect.anchoredPosition = Vector2.zero;

        float padding = 16f;

        if (Keyboard.current.rKey.wasPressedThisFrame && item.data.width != item.data.height)
        {
            iconRect.sizeDelta = new Vector2(h - padding, w - padding);
            iconRect.localEulerAngles = new Vector3(0f, 0f, 90f);
        }
        else
        {
            iconRect.sizeDelta = new Vector2(w - padding, h - padding);
            iconRect.localEulerAngles = Vector3.zero;
        }

        if (amountText != null)
        {
            amountText.gameObject.SetActive(item.data.isMagazine);

            if (item.data.isMagazine)
            {
                amountText.text = item.amount.ToString();
            }
        }
    }

    void Update()
    {
        if (!dragging) { return; }

        if (Keyboard.current.rKey.wasPressedThisFrame)
        {
            item.rotated = !item.rotated;
            Refresh();
        }

        Vector2 local;
        RectTransformUtility.ScreenPointToLocalPointInRectangle(
            inventory.GridArea, Mouse.current.position.ReadValue(), null, out local);

        Rect rect = inventory.GridArea.rect;
        float gridX = local.x - rect.xMin;
        float gridY = rect.yMax - local.y;

        float width = item.Width * cellSize + (item.Width - 1) * spacing;
        float height = item.Height * cellSize + (item.Height - 1) * spacing;

        float left = gridX - width / 2f;
        float top = gridY - height / 2f;

        ((RectTransform)transform).anchoredPosition = new Vector2(left, -top);

        targetX = Mathf.RoundToInt(left / (cellSize + spacing));
        targetY = Mathf.RoundToInt(top / (cellSize + spacing));

        background.color = inventory.CanPlace(item, targetX, targetY)
            ? normalColor
            : new Color(0.6f, 0.2f, 0.2f, 1f);
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        if (eventData.button != PointerEventData.InputButton.Left) { return; }

        dragging = true;
        originalRotated = item.rotated;
        targetX = item.x;
        targetY = item.y;

        transform.SetAsLastSibling();
        inventory.ClearInfo();
    }

    public void OnDrag(PointerEventData eventData)
    {
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        if (!dragging) { return; }

        dragging = false;

        if (inventory.CanPlace(item, targetX, targetY))
        {
            inventory.PlaceItem(item, targetX, targetY);
        }
        else
        {
            item.rotated = originalRotated;
        }

        background.color = normalColor;
        Refresh();
    }

    void OnDisable()
    {
        if (!dragging) { return; }

        dragging = false;
        item.rotated = originalRotated;
        background.color = normalColor;
        Refresh();
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        if (!dragging) { inventory.ShowInfo(item); }
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        inventory.ClearInfo();
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        if (eventData.button == PointerEventData.InputButton.Right)
        {
            inventory.UseItem(item);
        }
    }
}