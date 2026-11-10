using UnityEngine;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

namespace HollowHill
{
    /// <summary>
    /// Satu pintu masuk input yang jalan di Input System BARU maupun Input Manager LAMA.
    /// Unity 6 sering memakai Input System baru; memanggil Input.GetKey() di sana akan error.
    /// </summary>
    public static class HHInput
    {
        public static Vector2 Move()
        {
#if ENABLE_INPUT_SYSTEM
            var k = Keyboard.current;
            if (k == null) return Vector2.zero;
            float x = ((k.dKey.isPressed || k.rightArrowKey.isPressed) ? 1f : 0f) - ((k.aKey.isPressed || k.leftArrowKey.isPressed) ? 1f : 0f);
            float y = ((k.wKey.isPressed || k.upArrowKey.isPressed) ? 1f : 0f) - ((k.sKey.isPressed || k.downArrowKey.isPressed) ? 1f : 0f);
            return Vector2.ClampMagnitude(new Vector2(x, y), 1f);
#else
            return Vector2.ClampMagnitude(new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical")), 1f);
#endif
        }

        public static Vector2 PointerScreen()
        {
#if ENABLE_INPUT_SYSTEM
            return Mouse.current != null ? Mouse.current.position.ReadValue() : Vector2.zero;
#else
            return Input.mousePosition;
#endif
        }

        public static bool InteractDown()
        {
#if ENABLE_INPUT_SYSTEM
            return Keyboard.current != null && Keyboard.current.eKey.wasPressedThisFrame;
#else
            return Input.GetKeyDown(KeyCode.E);
#endif
        }

        public static bool FlashlightToggleDown()
        {
#if ENABLE_INPUT_SYSTEM
            return Keyboard.current != null && Keyboard.current.fKey.wasPressedThisFrame;
#else
            return Input.GetKeyDown(KeyCode.F);
#endif
        }

        public static bool FocusHeld()
        {
#if ENABLE_INPUT_SYSTEM
            return Mouse.current != null && Mouse.current.rightButton.isPressed;
#else
            return Input.GetMouseButton(1);
#endif
        }

        public static bool SprintHeld()
        {
#if ENABLE_INPUT_SYSTEM
            return Keyboard.current != null && Keyboard.current.leftShiftKey.isPressed;
#else
            return Input.GetKey(KeyCode.LeftShift);
#endif
        }
    }
}
