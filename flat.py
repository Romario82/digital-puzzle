import asyncio
from pathlib import Path
import flet as ft
import pazl


def prepare_data(text: str) -> str:
  pieces = [
    piece.strip()
    for piece in text.replace(',', '\n').split('\n')
    if piece.strip()
  ]
  return '\n'.join(pieces)


def read_file_content(path: str) -> str:
  return Path(path).read_text(encoding='utf-8')


def format_result(path: list[str], total_puzzle: str, total_pieces: int) -> tuple[str, str, str]:
  if not path:
    stats = f'Solution not found (fragments: {total_pieces})'
    sequence = ''
    answer = ''
  else:
    stats = f'Used fragments: {len(path)} of {total_pieces}'
    sequence = ' -> '.join(path)
    answer = total_puzzle
  return stats, sequence, answer


def main(page: ft.Page):
  page.title = 'Digital Puzzle'
  page.padding = 20
  page.window.width = 900
  page.window.height = 700

  status_text = ft.Text('Select a file with puzzle fragments', size=14)
  stats_text = ft.Text('', size=16, weight=ft.FontWeight.BOLD)
  progress = ft.ProgressRing(visible=False, width=24, height=24)

  path_field = ft.TextField(
    label='Fragment sequence',
    multiline=True,
    read_only=True,
    min_lines=4,
    max_lines=8,
    expand=True,
  )
  result_field = ft.TextField(
    label='Largest digital puzzle (answer)',
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
      stats_text.value = ''
      path_field.value = ''
      result_field.value = ''
      page.update()
      return

    status_text.value = f'Processing: {source_name} ({total_pieces} fragments)...'
    progress.visible = True
    open_button.disabled = True
    page.update()

    try:
      puzzle_path, total_puzzle = await asyncio.to_thread(pazl.solve_puzzle, data)
      stats, sequence, answer = format_result(puzzle_path, total_puzzle, total_pieces)

      status_text.value = f'File: {source_name}'
      stats_text.value = stats
      path_field.value = sequence
      result_field.value = answer
    except Exception as error:
      status_text.value = f'Error: {error}'
      stats_text.value = ''
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
    stats_text,
    path_field,
    result_field,
  )

def startflat():
    ft.run(main)

if __name__ == '__main__':
  ft.run(main)
