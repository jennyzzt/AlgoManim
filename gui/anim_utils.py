

# Formats text on animation blocks
def format_anim_block_str(metablock, sep='\n'):
    # extract metadata from the block
    meta = metablock.metadata

    return f"{meta.meta_name}{sep}" \
           f"#{meta.fid}"
