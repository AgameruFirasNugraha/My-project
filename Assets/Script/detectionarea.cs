using UnityEngine;

public class DetectionArea2D : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            Debug.Log("PLAYER CAUGHT!");
        }
    }
}