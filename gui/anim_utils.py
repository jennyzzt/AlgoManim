

# Formats text on animation blocks
def format_anim_block_str(metablock, sep='\n'):
    # extract metadata from the block
    meta = metablock.metadata

    w_prev = f"w_prev{sep}" if meta.w_prev else ""
    return f"{meta.meta_name}{sep}" \
           f"{w_prev}" \
           f"#{meta.fid}"
