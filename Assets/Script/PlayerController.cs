using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float walkSpeed = 2.5f;
    [SerializeField] private float sprintSpeed = 4.5f;
    [SerializeField] private float acceleration = 12f;
    [SerializeField] private float turnSpeed = 360f;

    private Rigidbody2D rb;
    private Camera cam;
    private Vector2 moveInput;
    private bool sprinting;

    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        cam = Camera.main;
    }

    void Update()
    {
        var kb = Keyboard.current;

        moveInput = Vector2.zero;
        if (kb.wKey.isPressed) moveInput += Vector2.up;
        if (kb.sKey.isPressed) moveInput += Vector2.down;
        if (kb.dKey.isPressed) moveInput += Vector2.right;
        if (kb.aKey.isPressed) moveInput += Vector2.left;
        moveInput = moveInput.normalized;

        sprinting = kb.leftShiftKey.isPressed;
    }

    void FixedUpdate()
    {
        float targetSpeed = sprinting ? sprintSpeed : walkSpeed;
        Vector2 targetVelocity = moveInput * targetSpeed;
        rb.linearVelocity = Vector2.MoveTowards(
            rb.linearVelocity, targetVelocity, acceleration * Time.fixedDeltaTime);

        Vector2 mouseWorld = cam.ScreenToWorldPoint(Mouse.current.position.ReadValue());
        Vector2 dir = mouseWorld - rb.position;
        float targetAngle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
        float newAngle = Mathf.MoveTowardsAngle(
            rb.rotation, targetAngle, turnSpeed * Time.fixedDeltaTime);
        rb.MoveRotation(newAngle);
    }
}
