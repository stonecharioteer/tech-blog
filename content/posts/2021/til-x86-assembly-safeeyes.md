---
date: 2021-03-03T10:00:00+05:30
draft: false
title: "TIL: x86 Assembly Programming and SafeEyes Break Reminder"
description: "Today I learned about fundamental x86 assembly programming concepts and SafeEyes, an extensible break reminder application to protect against eye strain during long coding sessions."
tags:
  - TIL
  - Assembly
  - x86
  - Low-level Programming
  - Health
  - Eye Care
  - Productivity
---

## x86 Assembly Programming Fundamentals

[A fundamental introduction to x86 assembly programming](https://www.nayuki.io/page/a-fundamental-introduction-to-x86-assembly-programming)

Comprehensive introduction to low-level programming with x86 assembly:

### Why Learn Assembly:
- **System Understanding**: How computers work at the lowest level
- **Performance Optimization**: Critical code optimization techniques
- **Debugging Skills**: Better understanding of compiled code behavior
- **Security Research**: Reverse engineering and vulnerability analysis
- **Embedded Systems**: Direct hardware programming capabilities

### x86 Architecture Basics:

#### **Registers:**
```assembly
; General-purpose registers (32-bit)
EAX - Accumulator (arithmetic operations)
EBX - Base (memory addressing)
ECX - Counter (loop operations)
EDX - Data (I/O operations)

; Pointer and index registers
ESP - Stack Pointer
EBP - Base Pointer (stack frame)
ESI - Source Index (string operations)
EDI - Destination Index (string operations)
```

#### **Memory Addressing:**
```assembly
; Direct addressing
mov eax, [0x1000]      ; Load from memory address

; Register indirect
mov eax, [ebx]         ; Load from address in EBX

; Base + displacement
mov eax, [ebx + 4]     ; Load from EBX + 4

; Index scaling
mov eax, [ebx + ecx*2] ; Array access with scaling
```

### Basic Instructions:

#### **Data Movement:**
```assembly
; Move operations
mov eax, 42          ; Load immediate value
mov ebx, eax         ; Copy register to register
mov [0x1000], eax    ; Store to memory

; Stack operations
push eax             ; Push EAX onto stack
pop ebx              ; Pop top of stack into EBX
```

#### **Arithmetic Operations:**
```assembly
; Basic arithmetic
add eax, ebx         ; EAX = EAX + EBX
sub eax, 10          ; EAX = EAX - 10
mul ebx              ; EAX = EAX * EBX (unsigned)
div ecx              ; EAX = EAX / ECX, EDX = remainder
```

#### **Control Flow:**
```assembly
; Comparisons and jumps
cmp eax, ebx         ; Compare EAX and EBX
je equal_label       ; Jump if equal
jne not_equal        ; Jump if not equal
jg greater_than      ; Jump if greater
jl less_than         ; Jump if less

; Unconditional jump
jmp some_label       ; Always jump
```

### Programming Patterns:

#### **Function Calls:**
```assembly
; Function prologue
push ebp             ; Save old base pointer
mov ebp, esp         ; Set up new stack frame

; Function epilogue
mov esp, ebp         ; Restore stack pointer
pop ebp              ; Restore base pointer
ret                  ; Return to caller
```

#### **Loop Structures:**
```assembly
; Simple loop
mov ecx, 10          ; Loop counter
loop_start:
    ; Loop body here
    dec ecx          ; Decrement counter
    jnz loop_start   ; Jump if not zero
```

### System Integration:
- **System Calls**: Interface with operating system services
- **Interrupts**: Handle hardware and software interrupts
- **Memory Management**: Direct memory allocation and manipulation
- **I/O Operations**: Hardware communication and device control

## SafeEyes - Eye Strain Prevention

[GitHub - slgobinath/SafeEyes](https://github.com/slgobinath/SafeEyes) - Protect your eyes from eye strain using this simple and beautiful, yet extensible break reminder

Essential tool for developers spending long hours at computers:

### The Problem:
- **Computer Vision Syndrome**: Eye strain from prolonged screen use
- **Reduced Blinking**: Screens cause reduced blink rate leading to dry eyes
- **Blue Light Exposure**: High-energy light affects sleep patterns
- **Poor Posture**: Extended screen time leads to neck and back problems

### SafeEyes Solution:

#### **Break Reminders:**
- **Short Breaks**: 20-second breaks every 20 minutes (20-20-20 rule)
- **Long Breaks**: 5-15 minute breaks every hour
- **Customizable**: Adjust timing based on your needs
- **Smart Scheduling**: Postpone breaks during presentations or calls

#### **Eye Exercises:**
- **Focus Exercises**: Look at distant objects to relax eye muscles
- **Blinking Reminders**: Conscious blinking to moisten eyes
- **Eye Movement**: Exercises to reduce eye muscle tension
- **Guided Instructions**: Step-by-step exercise guidance

### Features:

#### **Cross-Platform:**
- **Linux**: Native support with various desktop environments
- **Windows**: Full functionality on Windows systems
- **macOS**: Basic support for Mac users
- **Consistent Experience**: Similar features across platforms

#### **Customization:**
```python
# Example configuration
{
    "short_break_duration": 20,
    "short_break_interval": 1200,  # 20 minutes
    "long_break_duration": 300,    # 5 minutes
    "long_break_interval": 3600    # 1 hour
}
```

#### **Smart Features:**
- **Fullscreen Detection**: Pause during movies or presentations
- **Idle Detection**: Don't show breaks when away from computer
- **Notification System**: Gentle reminders without interruption
- **Statistics**: Track break compliance and eye health habits

### Health Benefits:

#### **Eye Health:**
- **Reduced Strain**: Regular breaks prevent eye fatigue
- **Better Focus**: Improved concentration after breaks
- **Moisture Maintenance**: Blinking exercises prevent dry eyes
- **Distance Vision**: Looking at distant objects relaxes eye muscles

#### **Overall Wellness:**
- **Posture Breaks**: Encourages movement and stretching
- **Mental Breaks**: Reduces cognitive load and stress
- **Sleep Quality**: Reduced blue light exposure before bedtime
- **Productivity**: Counter-intuitive but breaks improve overall output

### Plugin System:
- **Extensible Architecture**: Custom plugins for specific needs
- **Exercise Plugins**: Add new types of eye exercises
- **Notification Plugins**: Custom reminder methods
- **Integration**: Connect with other health and productivity apps

### Installation and Setup:
```bash
# Ubuntu/Debian
sudo apt install safeeyes

# Fedora
sudo dnf install safeeyes

# Arch Linux
sudo pacman -S safeeyes

# Or install from source
pip install safeeyes
```

Both resources address fundamental aspects of a developer's work - understanding how computers work at the deepest level and maintaining health during long coding sessions.