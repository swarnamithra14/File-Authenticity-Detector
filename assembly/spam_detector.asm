default rel

section .data
    fmt_spam db "SPAM DETECTED", 10, 0
    fmt_safe db "NO SPAM", 10, 0
    mode db "rb", 0

section .bss
    buffer resb 1000

section .text
    global main
    extern printf
    extern fopen
    extern fread
    extern fclose

main:
    sub rsp, 28h

    ; get argv[1]
    mov rax, rdx
    add rax, 8
    mov rdi, [rax]

    ; fopen(file, "rb")
    mov rcx, rdi
    lea rdx, [mode]
    call fopen

    mov rbx, rax

    ; fread(buffer, 1, 1000, file)
    lea rcx, [buffer]
    mov rdx, 1
    mov r8, 1000
    mov r9, rbx
    call fread

    ; fclose(file)
    mov rcx, rbx
    call fclose

    ; ==========================
    ; SPAM SCAN (look for 'w')
    ; ==========================
    lea rsi, [buffer]
    mov rcx, 1000

scan_loop:
    mov al, [rsi]

    ; check for 'w'
    cmp al, 'w'
    je spam

    ; check for 'f'
    cmp al, 'f'
    je spam

    inc rsi
    dec rcx
    jnz scan_loop

    ; SAFE
    lea rcx, [fmt_safe]
    call printf
    jmp end

spam:
    lea rcx, [fmt_spam]
    call printf

end:
    add rsp, 28h
    ret