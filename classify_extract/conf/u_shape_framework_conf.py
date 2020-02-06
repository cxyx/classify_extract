# coding: utf-8

relative_path_to_processor = '..app.processors'

processor_conf_list = [
    {
        'name': 'data_preprocess',
        'module': 'data_preprocess',
        'comment': 'offline数据预处理',
        'args': {}
    },
    {
        'name': 'content_to_text',
        'module': 'content_to_text',
        'comment': 'centent转text',
        'args': {}
    },
    {
        'name': 'classify_extract',
        'module': 'classify_extract',
        'comment': '',
        'args': {}
    },
    {
        'name': 'model_train',
        'module': 'model_train',
        'comment': '传递数据到文本分类模块',
        'args': {}
    },
]

workflow_conf_dict = {
    'offline': [
        'data_preprocess',
        'model_train',
    ],
    'online': [
        'content_to_text',
        'classify_extract',
    ]
}
