
using UnityEngine;

public class BatteryPickup : MonoBehaviour
{
    [Header("Battery Settings")]
    [SerializeField] private float batteryAmount = 25f;

    private void OnTriggerEnter2D(Collider2D other)
    {
        PlayerHealth player = other.GetComponentInParent<PlayerHealth>();

        if (player == null)
            return;

        Flashlight flashlight = player.GetComponentInChildren<Flashlight>();

        if (flashlight == null)
        {
            Debug.LogWarning("Flashlight component not found!");
            return;
        }

        flashlight.AddBattery(batteryAmount);

        Debug.Log("Battery collected! +" + batteryAmount);

        Destroy(gameObject);
    }
}
