from helper.aiu.load import load_knowledge_base, find_question_match, get_answer_for_question
from helper.cek_and_set import set_karakter_id

def obrolan_bot(input: str, karakter: str):
    if karakter.lower() == 'kusukabe tsumugi':
        base_pengetahuan: dict = load_knowledge_base('helper/aiu/dataset/kusukabeTsumugi.json')
    elif karakter.lower() == 'nurse-t':
        base_pengetahuan: dict = load_knowledge_base('helper/aiu/dataset/nurseT.json')
    elif karakter.lower() == 'kisara':
        base_pengetahuan: dict = load_knowledge_base('helper/aiu/dataset/kisara.jsonl')
    elif karakter.lower() == 'sayo':
        base_pengetahuan: dict = load_knowledge_base('helper/aiu/dataset/sayo.json')
    elif karakter.lower() == 'no 7':
        base_pengetahuan: dict = load_knowledge_base('helper/aiu/dataset/no7.json')
    elif karakter.lower() == 'tsukihime runa':
        return load_knowledge_base('helper/aiu/dataset/kisara.json')
    
    karakter_id = set_karakter_id(nama=karakter)
    if karakter_id == False:
        return {
            'status': False,
            'keterangan': 'karakter tidak valid'
        }
    
    questions: list = [question for item in base_pengetahuan.get("tanya-jawab", []) for question in item.get("tanya", [])]
    best_match: str | None = find_question_match(input, questions)
    
    if best_match:
        answer: str = get_answer_for_question(best_match, base_pengetahuan)
    
        
    return {
        'status': True,
        'keterangan': answer
    }