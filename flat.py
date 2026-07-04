import asyncio
from pathlib import Path
import flet as ft
import puzzle


def prepare_data(text: str) -> str:
  pieces = [
    piece.strip()
    for piece in text.replace(',', '\n').split('\n')
    if piece.strip()
  ]
  return '\n'.join(pieces)


def read_file_content(path: str) -> str:
  return Path(path).read_text(encoding='utf-8')


def main(page: ft.Page):
  page.title = 'Digital Puzzle'
  page.padding = 20
  page.window.width = 900
  page.window.height = 700

  status_text = ft.Text('Select a file with puzzle fragments', size=14)
  progress = ft.ProgressRing(visible=False, width=24, height=24)

  num_fragments_field = ft.TextField(
    label='Number of fragments used:',
    read_only=True,
    expand=True,
  )
  max_len_field = ft.TextField(
    label='Maximum sequence length in characters:',
    read_only=True,
    expand=True,
  )
  path_field = ft.TextField(
    label='Fragment order:',
    multiline=True,
    read_only=True,
    min_lines=4,
    max_lines=8,
    expand=True,
  )
  result_field = ft.TextField(
    label='Maximum sequence:',
    multiline=True,
    read_only=True,
    min_lines=6,
    expand=True,
  )

  async def process_text(text: str, source_name: str):
    data = prepare_data(text)
    total_pieces = len(data.splitlines())

    if total_pieces == 0:
      status_text.value = 'File is empty or contains no data'
      num_fragments_field.value = ''
      max_len_field.value = ''
      path_field.value = ''
      result_field.value = ''
      page.update()
      return

    status_text.value = f'Processing: {source_name} ({total_pieces} fragments)...'
    progress.visible = True
    open_button.disabled = True
    page.update()

    try:
      puzzle_path, total_puzzle = await asyncio.to_thread(puzzle.solve_puzzle, data)

      status_text.value = f'File: {source_name}'
      num_fragments_field.value = str(len(puzzle_path))
      max_len_field.value = str(len(total_puzzle))
      path_field.value = ' -> '.join(puzzle_path)
      result_field.value = total_puzzle
    except Exception as error:
      status_text.value = f'Error: {error}'
      num_fragments_field.value = ''
      max_len_field.value = ''
      path_field.value = ''
      result_field.value = ''
    finally:
      progress.visible = False
      open_button.disabled = False
      page.update()

  async def open_file(_: ft.Event[ft.Button]):
    result = await ft.FilePicker().pick_files(
      dialog_title='Select file with fragments',
      allowed_extensions=['txt'],
      file_type=ft.FilePickerFileType.CUSTOM,
      with_data=page.web,
    )
    if not result:
      return

    selected = result[0]
    if selected.path:
      text = await asyncio.to_thread(read_file_content, selected.path)
      await process_text(text, selected.name)
    elif selected.bytes is not None:
      text = selected.bytes.decode('utf-8')
      await process_text(text, selected.name)
    else:
      status_text.value = 'Failed to read the selected file'
      page.update()

  open_button = ft.FilledButton(
    'Open file',
    icon=ft.Icons.FOLDER_OPEN,
    on_click=open_file,
  )

  page.add(
    ft.Row(
      controls=[open_button, progress, status_text],
      spacing=12,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    ft.Row(
      controls=[num_fragments_field, max_len_field],
      spacing=12,
    ),
    path_field,
    result_field,
  )

def startflat():
    ft.run(main)

if __name__ == '__main__':
  ft.run(main)
