default rel

section .data
    fmt_pdf db "Detected: PDF file", 10, 0
    fmt_jpg db "Detected: JPG file", 10, 0
    fmt_png db "Detected: PNG file", 10, 0
    fmt_docx db "Detected: DOCX file", 10, 0
    fmt_unknown db "Unknown file type", 10, 0
    mode db "rb", 0

section .bss
    buffer resb 8

section .text
    global main
    extern printf
    extern fopen
    extern fread
    extern fclose

main:
    sub rsp, 28h

    ; get argv[1] (file path)
    mov rax, rdx
    add rax, 8
    mov rdi, [rax]

    ; fopen(file, "rb")
    mov rcx, rdi
    lea rdx, [mode]
    call fopen

    mov rbx, rax    ; file pointer

    ; fread(buffer, 1, 4, file)
    lea rcx, [buffer]
    mov rdx, 1
    mov r8, 4
    mov r9, rbx
    call fread

    ; fclose(file)
    mov rcx, rbx
    call fclose

    ; -------------------------
    ; CHECK PDF (%PDF = 25 50)
    ; -------------------------
    mov al, [buffer]
    cmp al, 0x25
    jne check_jpg

    mov al, [buffer+1]
    cmp al, 0x50
    jne check_jpg

    lea rcx, [fmt_pdf]
    call printf
    jmp end

check_jpg:
    ; -------------------------
    ; CHECK JPG (FF D8)
    ; -------------------------
    mov al, [buffer]
    cmp al, 0xFF
    jne check_png

    mov al, [buffer+1]
    cmp al, 0xD8
    jne check_png

    lea rcx, [fmt_jpg]
    call printf
    jmp end

check_png:
    ; -------------------------
    ; CHECK PNG (89 50)
    ; -------------------------
    mov al, [buffer]
    cmp al, 0x89
    jne check_docx

    mov al, [buffer+1]
    cmp al, 0x50
    jne check_docx

    lea rcx, [fmt_png]
    call printf
    jmp end

check_docx:
    ; -------------------------
    ; CHECK DOCX (PK = 50 4B)
    ; -------------------------
    mov al, [buffer]
    cmp al, 0x50
    jne unknown

    mov al, [buffer+1]
    cmp al, 0x4B
    jne unknown

    lea rcx, [fmt_docx]
    call printf
    jmp end

unknown:
    lea rcx, [fmt_unknown]
    call printf

end:
    add rsp, 28h
    ret