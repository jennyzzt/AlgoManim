

# Formats text on animation blocks
def format_anim_block_str(metablock, sep='\n'):
    # extract metadata from the block
    meta = metablock.metadata

    return f"{meta.meta_name}{sep}" \
           f"#{meta.fid}"


# Formats title of a customisation panel option
def format_customise_name(lower_meta):
    return f"{lower_meta.meta_name}: {lower_meta.val}"
