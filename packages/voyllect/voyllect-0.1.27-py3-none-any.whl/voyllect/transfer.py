#!/usr/bin/env python

import datetime
import glob
import os
import subprocess
import sys
import time

sys.path.append('..')


def generate_file_name(source_dict,
                       file_type, 
                       state):
    """Generates files names with the `state`.

    Args:
        source_dict (dict): dictionary containing the source information.
        file_type (str): type of file to stransfer.
        state (str): name of the state.
        
    Returns:
        str, Modified file name.
    """
    
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    return f"{timestamp}_{state}_{source_dict['source']}.{file_type}"


def generate_s3_object_name_inside_z00_ingest_zone(source_dict, 
                                                   state,
                                                   file_name,
                                                   custom_path):
    """Generates an object name in the z00-ingest zone.

    Args:
        source_dict (dict): dictionary containing the source information.
        state (str): name of the state.
        file_name (str): file name.
        custom_path (str): custom path for files in S3.

    Returns:
        str, Generated object name in the z00-ingest zone.
    """

    current_date = datetime.datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")

    return os.path.join(source_dict['source'], custom_path, state, year, month, file_name)


def send_files_to_s3(file_to_transfer_object_name, 
                     zone_name, 
                     file_to_transfer_s3_object_name,
                     region):
    """Sends `file_to_transfer_object_name` in AWS S3 bucket `zone_name`.

    Args:
        file_to_transfer_object_name (str): local object name to be transfered.
        zone_name (str): name of the AWS S3 bucket.
        file_name (str): generated AWS S3 object name in the bucket.
    """

    try:
        # print(f"[LOG] Attempting to transfer to S3: {file_to_transfer_object_name}")
        subprocess.run(["aws", "s3", "cp", 
                        file_to_transfer_object_name, 
                        os.path.join(f"s3://{zone_name}", file_to_transfer_s3_object_name).replace('\\', '/'),
                        "--region", region])
        # print(f"[LOG] Successfully transferred to S3 as: {file_to_transfer_s3_object_name}")
    except subprocess.CalledProcessError as e:
        print(f"[LOG] [EXCEPTION]\n{e}")


def transfer_state_files_to_s3(source_dict,
                               file_type, 
                               state, 
                               state_local_folder_path,
                               region,
                               custom_path=""):
    """Transfers the `state` files to AWS S3.
    
    Args:
        source_dict (dict): dictionary containing the source information.
        file_type (str): type of file to stransfer.
        state (str): name of the state.
        state_local_folder_path (str): folder path with the `state` files.
        custom_path (str): custom path for files in S3.
    """
    
    print(f"[LOG] Start to transfer files '{state}' to S3.")
    if sorted(glob.glob(os.path.join(state_local_folder_path, "*." + f"{file_type}"))):
        for state_local_object_name in \
            sorted(glob.glob(os.path.join(state_local_folder_path, "*." + f"{file_type}"))):
            new_generated_file_name = \
                generate_file_name(source_dict=source_dict, file_type=file_type, state=state)
            new_generated_s3_object_name = \
                generate_s3_object_name_inside_z00_ingest_zone(source_dict=source_dict, 
                                                                state=state, 
                                                                file_name=new_generated_file_name,
                                                                custom_path=custom_path)
            send_files_to_s3(file_to_transfer_object_name=state_local_object_name,
                             zone_name="voysen-z00-ingest-zone-eu-west-3",
                             file_to_transfer_s3_object_name=new_generated_s3_object_name,
                             region=region)
            time.sleep(2)
        print(f"[LOG] Files '{state}' have been transferred.")
    else:
        print(f"[LOG] There aren't any files '{state}' to transfer.")


def transfer_files_to_s3(source_dict,
                         aggregated_urls_folder_path,
                         aggregated_urls,
                         filtered_urls_folder_path,
                         filtered_urls,
                         urls_to_collect_folder_path,
                         urls_to_collect,
                         urls_to_collect_anchor_folder_path,
                         urls_to_collect_anchor,
                         aggregated_products_folder_path,
                         aggregated_products,
                         aggregated_reviews_folder_path,
                         aggregated_reviews,
                         counts_per_urls_folder_path,
                         counts_per_urls,
                         counts_per_collect_date_products_folder_path,
                         counts_per_collect_date_products,
                         counts_per_collect_date_reviews_folder_path,
                         counts_per_collect_date_reviews,
                         samples_products_folder_path,
                         samples_products,
                         samples_reviews_folder_path,
                         samples_reviews,
                         samples_urls_folder_path,
                         samples_urls):
    """Transfers files to S3.
    
    Args:
        source_dict (dict): dictionary containing the source information.
        aggregated_urls_folder_path (str): folder path to aggregated URLs.
        aggregated_urls (bool): transfer aggregated URLs.
        filtered_urls_folder_path (str): folder path to filtered URLs.
        filtered_urls (bool): transfer filtered URLs.
        urls_to_collect_folder_path (str): folder path to URLs to collect.
        urls_to_collect (bool): transfer URLs to collect.
        urls_to_collect_anchor_folder_path (str): folder path to URLs to collect anchor.
        urls_to_collect_anchor (bool): transfer URLs to collect anchor
        aggregated_products_folder_path (str): folder path to aggregated products.
        aggregated_products (bool): transfer aggregated products.
        aggregated_reviews_folder_path (str): folder path to aggregated reviews.
        aggregated_reviews (bool): transfer aggregated reviews.
        counts_per_urls_folder_path (str): folder path to KPIs files.
        counts_per_urls (bool): transfer KPIs files.
        counts_per_collect_date_products_folder_path (str): folder path to the products KPIs files.
        counts_per_collect_date_products (bool): transfer KPIs files.
        counts_per_collect_date_reviews_folder_path (str): folder path to the reviews KPIs files.
        counts_per_collect_date_reviews (bool): transfer KPIs files.
        samples_products_folder_path (str): folder path to the products KPIs files.
        samples_products (bool): transfer KPIs files.
        samples_reviews_folder_path (str): folder path to the reviews KPIs files.
        samples_reviews (bool): transfer KPIs files.
        samples_urls_folder_path (str): folder path to the URLs KPIs files.
        samples_urls (bool): transfer KPIs files.
    """

    # Aggregated URLs
    if aggregated_urls:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="json", 
                                   state='aggregated_urls', 
                                   state_local_folder_path=aggregated_urls_folder_path,
                                   region="eu-west-3")

    # Filtered URLs
    if filtered_urls:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="json",  
                                   state='filtered_urls', 
                                   state_local_folder_path=filtered_urls_folder_path,
                                   region="eu-west-3")
        
    # URLs to collect
    if urls_to_collect:
        transfer_state_files_to_s3(source_dict=source_dict, 
                                   file_type="json", 
                                   state='urls_to_collect', 
                                   state_local_folder_path=urls_to_collect_folder_path,
                                   region="eu-west-3")
        
    # URLs to collect anchor
    if urls_to_collect_anchor:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="json",  
                                   state='urls_to_collect_anchor', 
                                   state_local_folder_path=urls_to_collect_anchor_folder_path,
                                   region="eu-west-3")

    # Aggregated products
    if aggregated_products:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="json",  
                                   state='aggregated_products', 
                                   state_local_folder_path=aggregated_products_folder_path,
                                   region="eu-west-3")

    # Aggregated reviews
    if aggregated_reviews:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="json",  
                                   state='aggregated_reviews', 
                                   state_local_folder_path=aggregated_reviews_folder_path,
                                   region="eu-west-3")
    
    # counts_per_urls
    if counts_per_urls:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis", 
                                   state='counts_per_urls', 
                                   state_local_folder_path=counts_per_urls_folder_path,
                                   region="eu-west-3")
        
    # counts_per_collect_date_products
    if counts_per_collect_date_products:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis/counts_per_collect_date",  
                                   state='counts_per_collect_date_products', 
                                   state_local_folder_path=counts_per_collect_date_products_folder_path,
                                   region="eu-west-3")
        
    # counts_per_collect_date_reviews
    if counts_per_collect_date_reviews:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis/counts_per_collect_date/",  
                                   state='counts_per_collect_date_reviews', 
                                   state_local_folder_path=counts_per_collect_date_reviews_folder_path,
                                   region="eu-west-3")

    # samples_products
    if samples_products:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis/samples",  
                                   state='samples_products', 
                                   state_local_folder_path=samples_products_folder_path,
                                   region="eu-west-3")
        
    # samples_reviews
    if samples_reviews:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis/samples",  
                                   state='samples_reviews',
                                   state_local_folder_path=samples_reviews_folder_path,
                                   region="eu-west-3")
        
    # samples_urls
    if samples_urls:
        transfer_state_files_to_s3(source_dict=source_dict,
                                   file_type="xlsx",
                                   custom_path="kpis/samples",  
                                   state='samples_urls',
                                   state_local_folder_path=samples_urls_folder_path,
                                   region="eu-west-3")